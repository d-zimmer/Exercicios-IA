import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def criar_variaveis_entrada():
    angulo = ctrl.Antecedent(np.arange(-90, 91, 1), 'Angulo')
    velocidade_angular = ctrl.Antecedent(np.arange(-10, 11, 1), 'VelocidadeAngular')
    return angulo, velocidade_angular

def criar_variavel_saida():
    acao = ctrl.Consequent(np.arange(-100, 101, 1), 'Acao')
    return acao

def criar_conjuntos_fuzzy(angulo, velocidade_angular, acao):
    angulo['Inclinado para a Esquerda'] = fuzz.trimf(angulo.universe, [-90, -45, 0])
    angulo['Vertical'] = fuzz.trimf(angulo.universe, [-10, 0, 10])
    angulo['Inclinado para a Direita'] = fuzz.trimf(angulo.universe, [0, 45, 90])

    velocidade_angular['Deslocando-se para a Esquerda'] = fuzz.trimf(velocidade_angular.universe, [-10, -5, 0])
    velocidade_angular['Parado'] = fuzz.trimf(velocidade_angular.universe, [-2, 0, 2])
    velocidade_angular['Deslocando-se para a Direita'] = fuzz.trimf(velocidade_angular.universe, [0, 5, 10])

    acao['Empurre o carro fortemente para a Esquerda'] = fuzz.trimf(acao.universe, [-100, -50, 0])
    acao['Empurre o carro para a Esquerda'] = fuzz.trimf(acao.universe, [-50, 0, 50])
    acao['Não empurre o carro'] = fuzz.trimf(acao.universe, [-20, 0, 20])
    acao['Empurre o carro levemente para a Direita'] = fuzz.trimf(acao.universe, [0, 50, 100])
    acao['Empurre o carro fortemente para a Direita'] = fuzz.trimf(acao.universe, [50, 100, 100])

def criar_regras(angulo, velocidade_angular, acao):
    regra1 = ctrl.Rule(angulo['Inclinado para a Esquerda'] & velocidade_angular['Deslocando-se para a Esquerda'],
                       acao['Empurre o carro fortemente para a Esquerda'])
    # Adicione outras regras conforme necessário

def criar_sistema_controle(angulo, velocidade_angular, acao):
    regras = criar_regras(angulo, velocidade_angular, acao)
    sistema_controle = ctrl.ControlSystem(regras)
    controle = ctrl.ControlSystemSimulation(sistema_controle)
    return controle
