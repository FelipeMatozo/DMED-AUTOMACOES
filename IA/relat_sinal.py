import pandas as pd
from unidecode import unidecode

class TratarPlanilha:

    def __init__(self, data_path, claro_path):
        self.data_path = data_path
        self.claro_path = claro_path
        self.data_df = None
        self.claro_df = None
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

    def merge_planilhas(self):
        # Verificar se os DataFrames foram carregados
        if self.data_df is None or self.claro_df is None:
            raise ValueError("As planilhas ainda não foram carregadas. Execute o método 'carregar_planilhas' primeiro.")

        # Normalizar os nomes das colunas
        self.data_df = self.normalizar_nomes_colunas(self.data_df)
        self.claro_df = self.normalizar_nomes_colunas(self.claro_df)

        # Converter as colunas de chave para string
        self.data_df['Numero do RG'] = self.data_df['Numero do RG'].astype(str)
        self.claro_df['Numero de serie do medidor'] = self.claro_df['Numero de serie do medidor'].astype(str)

        # Realizar o merge usando as colunas especificadas
        self.merged_df = pd.merge(
            self.data_df,
            self.claro_df,
            left_on='Numero do RG',
            right_on='Numero de serie do medidor',
            how='inner'  # Pode mudar para 'left', 'right' ou 'outer' conforme a necessidade
        )
        print("Merge realizado com sucesso.")

        # Filtrar as linhas onde o valor da coluna "Sinal" é menor ou igual a -95
        if 'Sinal' in self.merged_df.columns:
            self.merged_df = self.merged_df[self.merged_df['Sinal'] <= -95]
            print("Filtro aplicado com sucesso.")

        # Remover colunas vazias
        self.merged_df = self.merged_df.dropna(axis=1, how='all')
        print("Colunas vazias removidas com sucesso.")

    def salvar_planilha(self, output_path='assets/excel/LES_CLARO.xlsx'):
        # Verificar se o merge foi realizado
        if self.merged_df is None:
            raise ValueError("Nenhum merge realizado. Execute o método 'merge_planilhas' primeiro.")

        # Remover as colunas especificadas
        colunas_para_remover = [
            "Obs.",
            "Ordem de Comun.",
            "NIO TM Hemera",
            "GD com beneficiaria BT",
            "Situacao da UC",
            "Conferencia de TM",
            "Leitura",
            "Conferencia de RG",
            "Situacao leitura",
            "SS comunicacao",
            "Prazo 621",
            "Situacao MS 693 ou 733",
            "Resultado",
            "conclusao MS 693 ou 733",
            "Regional 1",
            "Tipo do EQM",
            "Observacao conclusao MS 693 ou 733",
            "079 - MS 621, 675, 680, 693, 700 e 733 - MS 693 ou 733 emitidas no mes.Observa.1",
            "Observacao rejeicao MS 693 ou 733",
            "Marca_Hemera",
            "Telemetria 2",
            "Marca TM Hemera",
            "Marca TM",
            "SS de leitura no mes",
            "Observacao FIS aberta",
            "WF FIS aberta",
            "Fonte GD",
            "Observacao MS 621 conlcuida",
            "Conexao MS 621",
            "Modelo RG CIS",
            "Marca RG CIS",
            "Cli",
            "Mod",
            "Numero de serie do medidor",
            "Id Con",
            "Operadora",
            "IP usado SSN Ref",
            "Tot. Rec.",
            "Tot. Env.",
            "Ip Telemetria",
            "Tipo de Conexao",
            "Numero",
            "MS ano atual",
            "Id",
            "Id",
            "Comunicacao",
            "Resultado conclusao MS 693 ou 733",
            "Etapa",
            "Municipio2",
            "MED",
            "GD",
            "Protocolo",
            "Data Rec Telemetria",
            "Data Rec Chip",
            "Telemetria",
            "Conclusao MS 621",
            "Canais",
            "Chave",
            "Cliente",	
            "ENDERECO"
        ]

        # Normalizar os nomes das colunas no merged_df
        self.merged_df.columns = [unidecode(col).strip() for col in self.merged_df.columns]

        # Remover as colunas do DataFrame
        self.merged_df = self.merged_df.drop(columns=colunas_para_remover, errors='ignore')
        print("Colunas indesejadas removidas com sucesso.")

        # Reorganizar as colunas na ordem desejada
        colunas_desejadas = [
            "Clientes",
            "UC",
            "Sinal",
            "Nome da operadora",
            "Regional",
            "Municipio",
            "Numero do RG",
            "TM CIS",
            "Marca TM UC",
            "MIN",
            "SSN/MAC",
            "Nome",
            "Tipo de Porta de Conexao",
            "Data de Conexao",
            "Data de Desconexao",
            "Data da Ult. Mensagem",
            "Nome",
            "MIN",
            "SSN/MAC",
            "Marca TM UC"

        ]

        # Manter apenas as colunas desejadas e na ordem especificada
        self.merged_df = self.merged_df[colunas_desejadas]
        print("Colunas reorganizadas com sucesso.")

        # Salvar a planilha resultante
        self.merged_df.to_excel(output_path, index=False)
        print(f"Planilha resultante salva em: {output_path}")

# Utilização da classe com os caminhos fornecidos
planilha = TratarPlanilha('assets/excel/data.xlsx', 'assets/excel/Claro.xlsx')
planilha.carregar_planilhas()
planilha.merge_planilhas()
planilha.salvar_planilha()
