# Importações
import random
import math
import numpy as np
import pandas as pd
import requests
import time
import warnings
from deap import base, creator, tools, algorithms

# Suprimir todas as mensagens de aviso
warnings.filterwarnings("ignore")

# Função para calcular o retorno e o risco de um portfólio
def evaluate_portfolio(individual, data):
    """Calcula o retorno e o risco de um portfólio."""
    weights = np.array(individual)
    returns = np.sum(data.pct_change().mean() * weights) * 252
    volatility = np.sqrt(np.dot(weights.T, np.dot(data.pct_change().cov() * 252, weights)))
    return returns, volatility

# Função para obter os dados de preços de fechamento de ativos da Alpha Vantage
def get_alpha_vantage(symbols, api_key):
    """Obtém os dados de preços de fechamento de ativos da Alpha Vantage."""
    data = {}

    for symbol in symbols:
        base_url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': api_key
        }

        try:
            response = requests.get(base_url, params=params)
            raw_data = response.json()
            time_series = raw_data.get('Time Series (Daily)', {})

            # Armazena os dados em um dicionário
            data[symbol] = {date: float(info['4. close']) for date, info in time_series.items()}
        except Exception as e:
            print(f"Erro ao obter dados para {symbol}: {e}")

    return data

# Algoritmo Genético
def genetic_algorithm(n_assets, data):
    """Executa o Algoritmo Genético para otimização do portfólio."""
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", np.random.uniform, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=n_assets)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_portfolio, data=data)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
    toolbox.register("select", tools.selNSGA2)

    # Crie a população inicial
    population = toolbox.population(n=100)

    # Execute o algoritmo genético
    n_generations = 50

    for gen in range(n_generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.7, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        population = toolbox.select(offspring, len(population))

    # Recupere a solução ótima (portfólio)
    return tools.selBest(population, 1)[0]

# Função para o Simulated Annealing
def simulated_annealing(data, initial_solution, initial_temp, cooling_rate, num_iterations):
    """Executa o Simulated Annealing para otimização do portfólio."""
    current_solution = initial_solution
    current_cost = evaluate_portfolio(current_solution, data)
    best_solution = current_solution
    best_cost = current_cost
    temp = initial_temp

    for i in range(num_iterations):
        new_solution = current_solution.copy()

        # Perturbar a solução
        new_solution[random.randint(0, len(new_solution) - 1)] = np.random.uniform(0, 1)

        new_cost = evaluate_portfolio(new_solution, data)
        delta_cost = new_cost[0] - current_cost[0]

        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temp):
            current_solution = new_solution
            current_cost = new_cost

        if new_cost[0] < best_cost[0]:
            best_solution = new_solution
            best_cost = new_cost

        temp = exponential_decay(temp, cooling_rate)

    return best_solution, best_cost

# Função de resfriamento exponencial para o Simulated Annealing
def exponential_decay(temp, cooling_rate):
    """Função de resfriamento exponencial para o Simulated Annealing."""
    return temp * cooling_rate

def main():
    # Símbolos dos ativos que você deseja incluir no portfólio
    assets = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    n_assets = len(assets)

    # Substitua 'YOUR_API_KEY' pela sua chave de API Alpha Vantage
    api_key = '4KR9RHTR37YQ1XY5'

    # Obtém os dados de preços de fechamento dos ativos
    asset_data = get_alpha_vantage(assets, api_key)

    # Cria um DataFrame a partir dos dados obtidos
    data = pd.DataFrame(asset_data)

    start_time = time.time()
    best_portfolio = genetic_algorithm(n_assets, data)
    end_time = time.time()

    print("Melhor alocação de ativos:")
    print(assets)
    print(best_portfolio)
    best_return, best_risk = evaluate_portfolio(best_portfolio, data)
    print(f"Retorno anual: {best_return * 100:.2f}%")
    print(f"Risco anual: {best_risk * 100:.2f}%")
    print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

    # Parâmetros do Simulated Annealing
    initial_solution = np.random.random(n_assets)
    initial_temp = 1000
    cooling_rate = 0.995
    num_iterations = 10000

    start_time_sa = time.time()
    best_solution_sa, best_cost_sa = simulated_annealing(data, initial_solution, initial_temp, cooling_rate, num_iterations)
    end_time_sa = time.time()

    print("\nMelhor alocação de ativos (Simulated Annealing):")
    print(assets)
    print(best_solution_sa)
    best_return_sa, best_risk_sa = evaluate_portfolio(best_solution_sa, data)
    print(f"Retorno anual: {best_return_sa * 100:.2f}%")
    print(f"Risco anual: {best_risk_sa * 100:.2f}%")
    print(f"Tempo de execução (Simulated Annealing): {end_time_sa - start_time_sa:.2f} segundos")

if __name__ == "__main__":
    main()
