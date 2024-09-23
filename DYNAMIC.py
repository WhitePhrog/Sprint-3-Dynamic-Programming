import json
import pandas as pd


# Função para carregar o histórico
def carregar_historico(arquivo_json):
    try:
        with open(arquivo_json, 'r') as f:
            dados_historico = json.load(f)
        return dados_historico
    except FileNotFoundError:
        return {}


# Função para salvar o histórico
def salvar_historico(arquivo_json, dados_historico):
    with open(arquivo_json, 'w') as f:
        json.dump(dados_historico, f, indent=4)


# Função para o aluno registrar a performance
def registrar_performance_aluno(nome_aluno_input, nome_exercicio_input, porcentagem_conclusao, dados_historico):
    if nome_aluno_input not in dados_historico:
        dados_historico[nome_aluno_input] = {}
    dados_historico[nome_aluno_input][nome_exercicio_input] = {
        "conclusao": porcentagem_conclusao,
        "nota": None,
        "feedback": None
    }
    print(f"Performance de {porcentagem_conclusao}% registrada para o exercício {nome_exercicio_input}.")


# Função para exibir o histórico de um aluno em formato de tabela
def visualizar_historico_completo_aluno(nome_aluno_input, dados_historico):
    if nome_aluno_input in dados_historico:
        print(f"Histórico de {nome_aluno_input}:\n")

        # Criar dataframe a partir do histórico do aluno
        historico = []
        for nome_exercicio, detalhes in dados_historico[nome_aluno_input].items():
            historico.append([nome_exercicio, detalhes['conclusao'], detalhes['nota'], detalhes['feedback']])

        df = pd.DataFrame(historico, columns=['Exercício', 'Conclusão (%)', 'Nota', 'Feedback'])
        print(df.to_string(index=False))  # Exibir sem o índice do dataframe

        nome_exercicio_input = input(
            "\nDigite o nome do exercício que deseja ver o feedback ou pressione Enter para sair: ")
        if nome_exercicio_input and nome_exercicio_input in dados_historico[nome_aluno_input]:
            detalhes_exercicio = dados_historico[nome_aluno_input][nome_exercicio_input]
            nota = detalhes_exercicio["nota"] if detalhes_exercicio["nota"] is not None else "Não avaliado"
            feedback = detalhes_exercicio["feedback"] if detalhes_exercicio["feedback"] is not None else "Sem feedback"
            print(
                f"\nDetalhes do {nome_exercicio_input}: Conclusão {detalhes_exercicio['conclusao']}%, Nota {nota}, Feedback: {feedback}")
        elif nome_exercicio_input:
            print(f"Exercício {nome_exercicio_input} não encontrado.")
    else:
        print(f"Aluno {nome_aluno_input} não encontrado.")


# Função para o instrutor ver a lista de alunos
def listar_alunos(dados_historico):
    print("Lista de alunos:")
    for aluno in dados_historico.keys():
        print(aluno)


# Função para o instrutor visualizar o histórico de um aluno
def visualizar_historico_aluno(nome_aluno_input, dados_historico):
    if nome_aluno_input in dados_historico:
        print(f"Histórico de {nome_aluno_input}:\n")

        # Criar dataframe a partir do histórico do aluno
        historico = []
        for nome_exercicio, detalhes in dados_historico[nome_aluno_input].items():
            historico.append([nome_exercicio, detalhes['conclusao'], detalhes['nota'], detalhes['feedback']])

        df = pd.DataFrame(historico, columns=['Exercício', 'Conclusão (%)', 'Nota', 'Feedback'])
        print(df.to_string(index=False))  # Exibir sem o índice do dataframe

    else:
        print(f"Aluno {nome_aluno_input} não encontrado.")


# Função para o instrutor avaliar um exercício de um aluno
def avaliar_exercicio_aluno(nome_aluno_input, nome_exercicio_input, nota_dada, feedback_dado, dados_historico):
    if nome_aluno_input in dados_historico and nome_exercicio_input in dados_historico[nome_aluno_input]:
        dados_historico[nome_aluno_input][nome_exercicio_input]["nota"] = nota_dada
        dados_historico[nome_aluno_input][nome_exercicio_input]["feedback"] = feedback_dado
        print(f"Avaliação registrada para o exercício {nome_exercicio_input} do aluno {nome_aluno_input}.")
    else:
        print(f"Erro: Exercício {nome_exercicio_input} não encontrado para o aluno {nome_aluno_input}.")


# Carregar histórico
dados_historico_alunos = carregar_historico('historico.json')

# Loop principal
while True:
    tipo_usuario_input = input(
        "\nVocê está se conectando como (1) Aluno ou (2) Instrutor? Digite 'sair' para encerrar o programa: ")

    if tipo_usuario_input.lower() == 'sair':
        print("Encerrando o programa.")
        break

    if tipo_usuario_input == '1':
        # Aluno
        nome_aluno_input = input("Digite seu nome: ")
        while True:
            escolha_aluno = input(
                "\nDeseja (1) registrar um novo exercício ou (2) visualizar seu histórico? Digite 'voltar' para retornar: ")

            if escolha_aluno == 'voltar':
                break
            elif escolha_aluno == '1':
                nome_exercicio_input = input("Digite o nome do exercício: ")
                porcentagem_conclusao = float(input("Digite a porcentagem de conclusão do exercício (0 a 100): "))
                registrar_performance_aluno(nome_aluno_input, nome_exercicio_input, porcentagem_conclusao,
                                            dados_historico_alunos)
                salvar_historico('historico.json', dados_historico_alunos)
            elif escolha_aluno == '2':
                visualizar_historico_completo_aluno(nome_aluno_input, dados_historico_alunos)

    elif tipo_usuario_input == '2':
        # Instrutor
        while True:
            listar_alunos(dados_historico_alunos)
            nome_aluno_input = input("\nDigite o nome do aluno para visualizar o histórico ou 'voltar' para retornar: ")
            if nome_aluno_input.lower() == 'voltar':
                break
            visualizar_historico_aluno(nome_aluno_input, dados_historico_alunos)
            nome_exercicio_input = input("\nDigite o nome do exercício que deseja avaliar ou 'voltar' para retornar: ")
            if nome_exercicio_input.lower() == 'voltar':
                break
            nota_dada = float(input("Digite a nota (valor decimal) para o exercício: "))
            feedback_dado = input("Digite o feedback: ")
            avaliar_exercicio_aluno(nome_aluno_input, nome_exercicio_input, nota_dada, feedback_dado,
                                    dados_historico_alunos)
            salvar_historico('historico.json', dados_historico_alunos)
