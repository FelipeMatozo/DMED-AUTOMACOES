import os
import pandas as pd
from unidecode import unidecode
from geopy.distance import geodesic
from heapq import nsmallest
from banco_utils import buscar_dados, buscar_todos_dados, ver_exist

class TratarPlanilha:

    def __init__(self, data_path, planilha_path):
        self.data_path = data_path
        self.claro_path = planilha_path
        self.data_df = None
        self.planilha_df = None
        self.merged_df = None

    def carregar_planilhas(self):
        # Carregar as planilhas em DataFrames
        self.data_df = pd.read_excel(self.data_path)
        self.claro_df = pd.read_excel(self.claro_path)
        print("Planilhas carregadas com sucesso.")

    def normalizar_nomes_colunas(self, df):
        # Normalizar os nomes das colunas removendo acentos e caracteres especiais
        df.columns = [unidecode(col).strip() for col in df.columns]
        return df

    def padronizar_colunas(self, df, colunas):
        for coluna in colunas:
            df[coluna] = df[coluna].astype(str).str.strip().str.replace('.0', '', regex=False).replace('nan', '')


    def merge_planilhas(self,output_path='assets/excel/LES_TIM_merged.xlsx'):
        # Verificar se os DataFrames foram carregados
        if self.data_df is None or self.claro_df is None:
            raise ValueError("As planilhas ainda não foram carregadas. Execute o método 'carregar_planilhas' primeiro.")

        # Normalizar os nomes das colunas
        self.data_df = self.normalizar_nomes_colunas(self.data_df)
        self.claro_df = self.normalizar_nomes_colunas(self.claro_df)
        

        # Converter as colunas de chave para string
        self.data_df['Numero do RG'] = self.data_df['Numero do RG'].astype(str)
        self.claro_df['Numero de serie do medidor'] = self.claro_df['Numero de serie do medidor'].astype(str)
        self.padronizar_colunas(self.claro_df,["Numero de serie do medidor"])
        self.padronizar_colunas(self.data_df,["Numero do RG"])
        print(self.claro_df['Numero de serie do medidor'])
        print(self.data_df['Numero do RG'])
        # Realizar o merge usando as colunas especificadas
        self.merged_df = pd.merge(
            self.data_df,
            self.claro_df,
            left_on='Numero do RG',
            right_on='Numero de serie do medidor',
            how='inner'  # Pode mudar para 'left', 'right' ou 'outer' conforme a necessidade
        )
        print("Merge realizado com sucesso.")
        print(self.merged_df)
        self.merged_df.to_excel(output_path, index=False)

        # Filtrar as linhas onde o valor da coluna "Sinal" é menor ou igual a -95
        if 'Sinal' in self.merged_df.columns:
            self.merged_df = self.merged_df[self.merged_df['Sinal'] <= -95]
            print("Filtro aplicado com sucesso.")
            print(self.merged_df)

        # Remover colunas vazias
        # self.merged_df = self.merged_df.dropna(axis=1, how='all')
        print("Colunas vazias removidas com sucesso.")

    def salvar_planilha(self, output_path='assets/excel/LES_TIM.xlsx'):
        # Verificar se o merge foi realizado
        if self.merged_df is None:
            raise ValueError("Nenhum merge realizado. Execute o método 'merge_planilhas' primeiro.")

        # Remover as colunas indesejadas
        colunas_para_remover = [
            "Obs.", "Ordem de Comun.", "NIO TM Hemera", "GD com beneficiaria BT", 
            "Situacao da UC", "Conferencia de TM", "Leitura", "Conferencia de RG", 
            "Situacao leitura", "SS comunicacao", "Prazo 621", "Situacao MS 693 ou 733", 
            "Resultado", "conclusao MS 693 ou 733", "Regional 1", "Tipo do EQM", 
            "Observacao conclusao MS 693 ou 733", "079 - MS 621, 675, 680, 693, 700 e 733 - MS 693 ou 733 emitidas no mes.Observa.1", 
            "Observacao rejeicao MS 693 ou 733", "Marca_Hemera", "Telemetria 2", 
            "Marca TM Hemera", "Marca TM", "SS de leitura no mes", "Observacao FIS aberta", 
            "WF FIS aberta", "Fonte GD", "Observacao MS 621 conlcuida", "Conexao MS 621", 
            "Modelo RG CIS", "Marca RG CIS", "Cli", "Mod", "Numero de serie do medidor", 
            "Id Con", "Operadora", "IP usado SSN Ref", "Tot. Rec.", "Tot. Env.", 
            "Ip Telemetria", "Tipo de Conexao", "Numero", "MS ano atual", "Id", 
            "Id", "Comunicacao", "Resultado conclusao MS 693 ou 733", "Etapa", 
            "Municipio2", "MED", "GD", "Protocolo", "Data Rec Telemetria", 
            "Data Rec Chip", "Telemetria", "Conclusao MS 621", "Canais", 
            "Chave", "Cliente", "ENDERECO","Marca TM UC","MIN","SSN/MAC"
        ]

        # Normalizar os nomes das colunas no merged_df
        self.merged_df.columns = [unidecode(col).strip() for col in self.merged_df.columns]

        # Remover as colunas do DataFrame
        self.merged_df = self.merged_df.drop(columns=colunas_para_remover, errors='ignore')
        print("Colunas indesejadas removidas com sucesso.")

        self.merged_df.to_excel(output_path, index=False)
        print(f"Planilha resultante salva em: {output_path}")

        # Processar antenas para cada UC na tabela resultante
        self.processar_antenas(output_path)

    def buscar_lat_lon(self, uc):
        resultado = buscar_dados("UC_LAT_LONG", "UC", uc, ["LATITUDE", "LONGITUDE"])
        
        if resultado:
            latitude, longitude = resultado
            return float(latitude), float(longitude)
        else:
            return None

    def encontrar_antenas_mais_proximas(self, uc_lat, uc_lon, n=3):
        colunas = ["latitude_antena", "longitude_antena", "operadora", "estacao"]
        antenas = buscar_todos_dados("antenas_parana", colunas)

        distancias_antenas = []
        
        for antena_lat, antena_lon, operadora, estacao in antenas:
            distancia = geodesic((uc_lat, uc_lon), (antena_lat, antena_lon)).kilometers
            distancias_antenas.append((distancia, (operadora, estacao)))

        antenas_mais_proximas = nsmallest(n, distancias_antenas, key=lambda x: x[0])
        
        return [
            (antena[1][0], antena[1][1], f"{antena[0]:.2f} km")
            for antena in antenas_mais_proximas
        ]

    def processar_antenas(self, output_path):
        resultados = []

        for index, row in self.merged_df.iterrows():
            numero_uc = row["UC"]
            if ver_exist("UC_LAT_LONG", "UC", numero_uc):
                print(f'A UC: {numero_uc} está presente no banco de dados!')
                latitude_uc, longitude_uc = self.buscar_lat_lon(numero_uc)

                if latitude_uc is not None and longitude_uc is not None:
                    antenas_proximas = self.encontrar_antenas_mais_proximas(latitude_uc, longitude_uc)

                    if antenas_proximas:
                        resultado_row = [numero_uc]
                        for antena in antenas_proximas:
                            resultado_row.append(f"{antena[0]} ({antena[1]})")
                            resultado_row.append(antena[2])
                        resultados.append(resultado_row)
                    else:
                        print(f"Nenhuma antena encontrada próxima à UC {numero_uc}.")
                else:
                    print(f'Não foi possível encontrar as coordenadas para a UC: {numero_uc}.')
            else:
                print(f'A UC: {numero_uc} NÃO está presente no banco de dados!')

        # Criar um DataFrame com os resultados das antenas
        colunas_resultados = ["UC", "Antena 1", "Distância 1", "Antena 2", "Distância 2", "Antena 3", "Distância 3"]
        df_resultados = pd.DataFrame(resultados, columns=colunas_resultados)

        # Salvar os resultados em uma nova planilha
        resultado_path = os.path.join(os.path.dirname(output_path), "resultados_antenas.xlsx")
        df_resultados.to_excel(resultado_path, index=False)
        print(f"Resultados de antenas salvos em: {resultado_path}")

    def merge_com_planilha_antenas(self, antennas_path, output_path='assets/excel/Final_sinal_op/final_TIM_CATIVOS.xlsx'):
        # Carregar a planilha de antenas
        antennas_df = pd.read_excel(antennas_path)

        # Verificar se o merged_df foi realizado
        if self.merged_df is None:
            raise ValueError("Nenhum merge realizado. Execute o método 'merge_planilhas' primeiro.")

        # Realizar o merge com a planilha de antenas usando a coluna "UC"
        resultado_final = pd.merge(self.merged_df, antennas_df, on='UC', how='left')  # Usar 'left' para manter todas as linhas de merged_df

        # Reorganizar as colunas na ordem desejada
        colunas_desejadas = [
            "Clientes", "UC", "Sinal", "Nome da operadora", "Regional", 
            "Municipio", "Antena 1", "Distância 1", "Antena 2", "Distância 2", 
            "Antena 3", "Distância 3", "Numero do RG", "Nome","TM CIS", 
            "Tipo de Porta de Conexao", "Data de Conexao", 
            "Data de Desconexao", "Data da Ult. Mensagem"
        ]

        # Manter apenas as colunas desejadas que estão presentes no DataFrame
        colunas_presentes = [col for col in colunas_desejadas if col in resultado_final.columns]
        resultado_final = resultado_final[colunas_presentes]
        print("Colunas reorganizadas com sucesso.")

        # Salvar o resultado final
        resultado_final.to_excel(output_path, index=False)
        print(f"Planilha final salva em: {output_path}")


if __name__ == "__main__":
    tratar = TratarPlanilha("assets/excel/LES_CATIVOS.xlsx", "assets/excel/TIM.xlsx")
    tratar.carregar_planilhas()
    tratar.merge_planilhas()
    tratar.salvar_planilha()
    # Caminho para a planilha de resultados de antenas
    resultados_antenas_path = "assets/excel/resultados_antenas.xlsx"
    
    # Realizar o merge com a planilha de antenas
    tratar.merge_com_planilha_antenas(resultados_antenas_path)