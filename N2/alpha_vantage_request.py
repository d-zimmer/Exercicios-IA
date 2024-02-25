import requests

# Substitua 'YOUR_API_KEY' pela sua chave de API Alpha Vantage
api_key = '4KR9RHTR37YQ1XY5'

# Símbolo do ativo que você deseja obter os dados
symbol = 'AAPL'

# Função para obter os dados do Alpha Vantage
def get_alpha_vantage_data(symbol, api_key):
    base_url = 'https://www.alphavantage.co/query'
    
    # Parâmetros da consulta
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Os dados retornados estão sob a chave 'Time Series (Daily)'
        time_series = data.get('Time Series (Daily)', {})
        return time_series
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return None

# Chama a função para obter os dados
data = get_alpha_vantage_data(symbol, api_key)

if data:
    # Exibe os dados de preços de fechamento para o símbolo especificado
    for date, info in data.items():
        print(f"Data: {date}, Preço de Fechamento: {info['4. close']}")
