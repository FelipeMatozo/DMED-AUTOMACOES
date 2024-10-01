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

def add_subs_banco(nome_tabela, colunas, valores):
    """
    Adiciona ou substitui dados em uma tabela no banco de dados. 
    Cria a tabela se ela não existir, com a primeira coluna fornecida como chave primária.
    
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

    # Usar `INSERT OR REPLACE` para inserir ou substituir os dados existentes
    consulta_insercao = f"INSERT OR REPLACE INTO {nome_tabela} ({colunas_str}) VALUES ({placeholders})"
    cursor.execute(consulta_insercao, valores)
    con.commit()

    print(f"Dados inseridos/substituídos com sucesso na tabela {nome_tabela}: {valores}.")

    con.close()

def ver_exist(TABELA, COLUNA, DADO):
    """
    Verifica a existência do dado na tabela.
    
    Parâmetros:
    NOME_TABELA (str): O nome da tabela no banco de dados.
    COLUNA: Nome da coluna a ser verificada.

    Retorna:
    Retorna True se o dado existir, False caso contrário.
    """
    # Conectar ao banco de dados
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    # Verificar se o dado existe na tabela
    cursor.execute(f"SELECT COUNT(*) FROM {TABELA} WHERE {COLUNA} = ?", (DADO,))
    resultado = cursor.fetchone()[0]

    # Fechar a conexão com o banco de dados
    conexao.close()

    # Se o dado não for encontrado, adicionar ao arquivo de texto
    if resultado == 0:
        caminho_txt = os.path.join('assets\\txt\\ucs_nao_encontradas.txt')
        with open(caminho_txt, 'a') as arquivo:
            arquivo.write(f"{DADO}\n")
    
    # Retornar True se o dado existir, False caso contrário
    return resultado > 0

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


def exportar_para_excel(tabela, coluna, valores, caminho_arquivo_excel):
    """
    Exporta os dados de uma tabela do banco de dados filtrando por uma lista de valores de uma coluna específica e exporta para um arquivo Excel.
    
    Parâmetros:
    tabela (str): Nome da tabela do banco de dados.
    coluna (str): Nome da coluna para filtrar os dados.
    valores (list): Lista de valores da coluna para filtrar os dados.
    caminho_arquivo_excel (str): Caminho completo para salvar o arquivo Excel.
    """
    # Conectar ao banco de dados
    con = sqlite3.connect(CAMINHO_BANCO)

    # Imprimir os valores originais
    print("Valores:", valores)

  

    # Criar um DataFrame vazio para armazenar todos os dados
    df_total = pd.DataFrame()

    # Iterar sobre os valores tratados
    for valor in valores:
        # Criar a consulta SQL para o valor atual
        query = f"SELECT * FROM {tabela} WHERE {coluna} = ?"
        
        # Executar a consulta
        df = pd.read_sql_query(query, con, params=[valor])
        
        # Verificar se há dados a serem exportados
        if not df.empty:
            df_total = pd.concat([df_total, df])  # Adicionar os dados ao DataFrame total
            print(f"Dados encontrados e adicionados para {valor}.")
        else:
            print(f"Nenhum dado encontrado para o valor {valor}.")
    
    # Verificar se há dados para exportar no DataFrame total
    if not df_total.empty:
        # Exportar os dados acumulados para um arquivo Excel
        df_total.to_excel(caminho_arquivo_excel, index=False)
        print(f"Dados exportados com sucesso para {caminho_arquivo_excel}.")
    else:
        print("Nenhum dado encontrado para os valores fornecidos.")
    
    # Fechar a conexão
    con.close()


    ############ COMO USAR ##############
    # exportar_para_excel('TABELA', 'COLUNA', VALORES, 'caminho/do/arquivo.xlsx')
    #####################################