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

        

    def salvar_excel(self, output_path='assets/excel/coordenadas_tratadas.xlsx'):
        self.data_df.to_excel(output_path, index=False)
        print(f"Planilha resultante salva em: {output_path}")

    def separa_coluna(self, coluna):
        # Verifica se a coluna existe no DataFrame
        if coluna not in self.data_df.columns:
            raise ValueError(f"A coluna '{coluna}' não existe no DataFrame.")

        # Separa a coluna em duas novas colunas
        novas_colunas = self.data_df[coluna].str.split(',', expand=True)

        # Renomeia as novas colunas
        novas_colunas.columns = [f"LATITUDE", f"LONGITUDE"]

        # Adiciona as novas colunas ao DataFrame
        self.data_df = pd.concat([self.data_df, novas_colunas], axis=1)
        self.data_df = self.data_df.drop(columns="COORD_GOOGLE", errors='ignore')

    def adiciona_banco(self):
        # Nome da tabela no banco de dados
        nome_tabela = 'UC_LAT_LONG'

        # Colunas a serem inseridas
        colunas = ['UC', 'LATITUDE', 'LONGITUDE']

        # Loop através do DataFrame e insira os dados no banco de dados
        for index, row in self.data_df.iterrows():
            valores = (row['UC'], row['LATITUDE'], row['LONGITUDE'])
            add_subs_banco(nome_tabela, colunas, valores)

if __name__ == "__main__":
    tratar= TratarPlanilha(data_path="assets\\excel\\Coordenadas.xlsx")
    tratar.carregar_planilhas()
    tratar.normalizar_nomes_colunas()
    tratar.separa_coluna(coluna="COORD_GOOGLE")
    tratar.salvar_excel()
    tratar.adiciona_banco()