############## COMO USAR ##############

# from banco_utils import add_banco

# # Parâmetros para adicionar dados
# nome_tabela = "IRIS"
# colunas = ["UC", "ID", "CODIGO_DO_PONTO", "PORTA_TM"]
# valores = ("12345", "001", "Ponto01", "TM01")

# # Chamar a função add_banco
# add_banco(nome_tabela, colunas, valores)

########################################


import os
import sqlite3
import pandas as pd
script_dir = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(script_dir, '..', 'banco', 'banco_dmed.db')

def add_banco(nome_tabela, colunas, valores):
    """
    Adiciona dados a uma tabela no banco de dados. Cria a tabela se ela não existir,
    com a primeira coluna fornecida como chave primária.
    
    Parâmetros:
    nome_tabela (str): Nome da tabela onde os dados serão inseridos.
    colunas (list): Lista com os nomes das colunas onde os dados serão inseridos.
    valores (tuple): Tupla com os valores correspondentes às colunas.
    """
    con = sqlite3.connect(CAMINHO_BANCO)
    cursor = con.cursor()

    # Formatar as colunas e placeholders para o SQL
    colunas_str = ", ".join(colunas)
    placeholders = ", ".join("?" for _ in colunas)

    # Criar a tabela se ela não existir, com a primeira coluna como chave primária
    colunas_definicao = f"{colunas[0]} TEXT PRIMARY KEY, " + ", ".join([f"{coluna} TEXT" for coluna in colunas[1:]])
    consulta_criacao = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({colunas_definicao})"
    cursor.execute(consulta_criacao)

    # Verifica se o dado já existe apenas na coluna da chave primária (primeira coluna)
    chave_primaria = colunas[0]  # Primeira coluna é a chave primária
    valor_chave_primaria = (valores[0],)

    # Criar a consulta para verificação de duplicidade pela chave primária
    consulta_selecao = f"SELECT {chave_primaria} FROM {nome_tabela} WHERE {chave_primaria} = ?"
    
    cursor.execute(consulta_selecao, valor_chave_primaria)
    existing_entry = cursor.fetchone()

    if not existing_entry:
        # Inserir os dados
        consulta_insercao = f"INSERT INTO {nome_tabela} ({colunas_str}) VALUES ({placeholders})"
        cursor.execute(consulta_insercao, valores)
        con.commit()
        print(f"Dados inseridos com sucesso na tabela {nome_tabela}: {valores}.")
    else:
        print(f"Dados já existentes na tabela {nome_tabela} para {chave_primaria}: {valor_chave_primaria}.")
    
    con.close()

    ############## COMO USAR ##############

    # from banco_utils import add_banco

    # # Parâmetros para adicionar dados
    # nome_tabela = "IRIS"
    # colunas = ["UC", "ID", "CODIGO_DO_PONTO", "PORTA_TM"]
    # valores = ("12345", "001", "Ponto01", "TM01")

    # # Chamar a função add_banco
    # add_banco(nome_tabela, colunas, valores)

    ########################################

def buscar_dados(nome_tabela, coluna_filtro, valor_filtro, colunas_retorno):
    """
    Busca dados de maneira dinâmica no banco de dados.
    
    Parâmetros:
    nome_tabela (str): Nome da tabela a ser consultada.
    coluna_filtro (str): Nome da coluna para o filtro WHERE.
    valor_filtro (str): Valor a ser filtrado.
    colunas_retorno (list): Lista de colunas que deseja obter no resultado.
    
    Retorna:
    tuple: Os valores das colunas selecionadas ou None se não encontrar.
    """
    # Conectar ao banco de dados
    con = sqlite3.connect(CAMINHO_BANCO)
    cursor = con.cursor()

    # Montar a consulta SQL dinamicamente
    colunas_str = ", ".join(colunas_retorno)
    consulta = f"SELECT {colunas_str} FROM {nome_tabela} WHERE {coluna_filtro} = ?"
    
    # Executar a consulta
    cursor.execute(consulta, (valor_filtro,))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    con.close()

    return resultado

    ############ COMO USAR ##############

    # resultado = buscar_dados("NOME_TABELA", "COLUNA_REFERÊNCIA", dado_da_coluna, ["COLUNA_RETORNO", "COLUNA_RETORNO"])
    
    #####################################

def buscar_todos_dados(nome_tabela, colunas):
    """
    Busca todos os dados de uma tabela no banco de dados.
    
    Parâmetros:
    nome_tabela (str): O nome da tabela no banco de dados.
    colunas (list): Lista com os nomes das colunas a serem selecionadas.

    Retorna:
    list: Uma lista de tuplas contendo os valores das colunas especificadas.
    """
    # Conectar ao banco de dados
    con = sqlite3.connect(CAMINHO_BANCO)
    cursor = con.cursor()

    # Formatar a consulta com base nas colunas fornecidas
    colunas_str = ", ".join(colunas)
    consulta = f"SELECT {colunas_str} FROM {nome_tabela}"
    
    # Executar a consulta
    cursor.execute(consulta)
    dados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    con.close()

    return dados

    ############ COMO USAR ##############

    # COLUNAS_DESEJADAS = ["Coluna1", "Coluna2", "Coluna3"]
    # DADOS_DE_ALGO = buscar_todos_dados("NOME_TABELA", COLUNAS_DESEJADAS)
    
    #####################################

def exportar_para_excel(tms_lista, caminho_arquivo_excel):
    """
    Exporta os dados da tabela IRIS filtrando por uma lista de valores 'codigo_tm' e exporta para um arquivo Excel.
    
    Parâmetros:
    tms_lista (list): Lista de valores da coluna 'codigo_tm' para filtrar os dados.
    caminho_arquivo_excel (str): Caminho completo para salvar o arquivo Excel.
    """
    # Conectar ao banco de dados
    con = sqlite3.connect(CAMINHO_BANCO)
    
    # Separar os valores da string e adicionar '00' na frente de cada TM
    tms_lista_tratata = ['00' + tm for tm in tms_lista.split()]
    print(tms_lista_tratata)
    
    # Criar a consulta SQL com base na lista de TM's
    placeholders = ', '.join('?' for _ in tms_lista_tratata)  # Criar placeholders para a consulta
    query = f"SELECT * FROM IRIS WHERE codigo_tm IN ({placeholders})"
    
    # Executar a consulta com base na lista de TM's
    df = pd.read_sql_query(query, con, params=tms_lista_tratata)
    
    # Verificar se há dados a serem exportados
    if not df.empty:
        # Exportar os dados para um arquivo Excel
        df.to_excel(caminho_arquivo_excel, index=False)
        print(f"Dados exportados com sucesso para {caminho_arquivo_excel}.")
    else:
        print(f"Nenhum dado encontrado para os TM's fornecidos.")
    
    # Fechar a conexão
    con.close()