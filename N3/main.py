from pendulo_invertido import criar_variaveis_entrada, criar_variavel_saida, criar_conjuntos_fuzzy, criar_sistema_controle

if __name__ == "__main__":
    # Criar variáveis de entrada e saída
    angulo, velocidade_angular = criar_variaveis_entrada()
    acao = criar_variavel_saida()

    # Criar conjuntos fuzzy
    criar_conjuntos_fuzzy(angulo, velocidade_angular, acao)

    # Criar sistema de controle
    sistema_controle = criar_sistema_controle(angulo, velocidade_angular, acao)

    # Exemplo de execução do sistema
    sistema_controle.input['angulo'] = -30
    sistema_controle.input['VelocidadeAngular'] = -8
    sistema_controle.compute()
    resultado = sistema_controle.output['Acao']
    print(f"Ação resultante: {resultado}")
    
    
    
    
    
    
    
    
    
Desenvolver um Sistema de Inferência Fuzzy para gerenciar a estabilidade de um pêndulo invertido montado sobre um carro.
A Modelagem do Problema é composto pelas seguintes etapas:
    1.Determinar um conjunto de regras fuzzy
    2.Fuzzyficar as entradas usando as funções de associação de entrada
    3.Combinar as entradas fuzzyficadas de acordo com as regras fuzzy para estabelecer uma “força” de regra
    4.Encontrar a consequência da regra combinando a força da regra e a função de pertinência da saída (se for um FIS Mamdani)
    5.Combinar as consequências para obter uma distribuição de saída
    6.Defuzzyficar a distribuição da saída (esta etapa aplica-se somente se uma saída crisp for necessária).
    
Depois de determinar as entradas e saídas apropriadas para sua aplicação, há três etapas para projetar os parâmetros para um sistema fuzzy:
    1. Especifique os conjuntos fuzzy a serem associados a cada variável
    2. Decida o que as regras fuzzy vão ser
    3. Especifique a forma das funções de pertinência.
    
Podemos começar a projetar um sistema fuzzy subdividindo-se o problema em duas variáveis de entrada, referentes ao pêndulo invertido (ângulo do pêndulo e velocidade angular), em conjuntos de pertinência.
O ângulo pode ser descrito como:
    1.Inclinadopara a esquerda (N)
    2.Vertical(Z)
    3.Inclinadopara a direita (P)

A velocidade angular pode ser descrita como:
    1.Deslocando-se para a esquerda (N)
    2.Parado(Z)
    3.Deslocando-se para a direita (P)