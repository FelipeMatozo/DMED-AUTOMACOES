'''
# Adiciona o caminho do diretório principal (SISTEMA_RPA_DMED) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_dir = os.path.dirname(os.path.abspath(__file__))
script_cor = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from apps.utils.banco_utils import buscar_dados, buscar_todos_dados, ver_exist
'''
import os
import sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(script_dir, '..', '..', 'banco', 'banco_dmed.db')

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

    """
    ############## COMO USAR ##############
    # Parâmetros para adicionar dados
    nome_tabela = "IRIS"
    colunas = ["UC", "ID", "CODIGO_DO_PONTO", "PORTA_TM"]
    valores = ("12345", "001", "Ponto01", "TM01")

    # Chamar a função add_banco
    add_banco(nome_tabela, colunas, valores)
    """
    

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

    # Retornar True se o dado existir, False caso contrário
    return resultado > 0

    ############ COMO USAR ##############

    # ver_exist("NOME_TABELA","COLUNA", "DADO")

    #####################################