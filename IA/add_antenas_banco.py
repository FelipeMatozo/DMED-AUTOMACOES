import os
import pandas as pd
from unidecode import unidecode
from geopy.distance import geodesic
from heapq import nsmallest
from banco_utils import buscar_dados, buscar_todos_dados, ver_exist, add_subs_banco

class TratarPlanilha:

    def __init__(self, data_path):
        self.data_path = data_path
        self.data_df = None
       
        

    def carregar_planilhas(self):
        # Carregar as planilhas em DataFrames
        self.data_df = pd.read_excel(self.data_path)

    def normalizar_nomes_colunas(self):
        # Normalizar os nomes das colunas removendo acentos e caracteres especiais
        self.data_df.columns = [unidecode(col).strip() for col in self.data_df.columns]
        return self.data_df


    def adiciona_banco(self):
        # Nome da tabela no banco de dados
        nome_tabela = 'parana_antenas'

        # Colunas a serem inseridas
        colunas = ['estacao', 'operadora', 'latitude_antena','longitude_antena','tecnologia','faixa']

        # Loop através do DataFrame e insira os dados no banco de dados
        for index, row in self.data_df.iterrows():
            valores = (row['estacao'], row['operadora'], row['latitude_antena'], row['longitude_antena'], row['tecnologia'], row['faixa'])
            add_subs_banco(nome_tabela, colunas, valores)

if __name__ == "__main__":
    tratar= TratarPlanilha(data_path="assets\\excel\\antenas_parana.xlsx")
    tratar.carregar_planilhas()
    tratar.adiciona_banco()