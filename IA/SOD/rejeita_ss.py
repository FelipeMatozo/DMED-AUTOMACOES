import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, base_dir)
from IA.ReconhecimentoDeImagem import Reconhecimento
import pandas as pd
import pyautogui as py
from time import time, sleep
from datetime import datetime
class SOD:
    
    def __init__(self):
        self.ia=Reconhecimento(numeroDeTentativasMax=5, delay=0.9)
    def hora_atual(self):
         # Parse a string de data e hora
            # Obter a hora atual
            agora = datetime.now()
            # Formatar a hora para o formato desejado
            hora_min = agora.strftime("%d%m%Y%H%M")
            return hora_min
    
class inf_planilha:
    """Tudo relacionado à planilha vai ficar aqui"""
    def __init__(self, caminho_planilha):
        self.caminho_planilha = caminho_planilha
        self.dados = None
        self.carregar_dados()
    
    def carregar_dados(self, coluna=None):
        """
        Carrega os dados da planilha
        
        :param coluna: Nome ou índice da coluna a ser carregada. 
                       Se None, carrega toda a planilha.
        """
        try:
            # Lê os dados da planilha
            planilha = pd.read_excel(self.caminho_planilha)

            # Carrega toda a planilha ou uma coluna específica
            if coluna is not None:
                if isinstance(coluna, int):
                    # Se for índice, pega a coluna pelo índice
                    self.dados = planilha.iloc[:, coluna]
                else:
                    # Se for nome, pega a coluna pelo nome
                    self.dados = planilha[coluna]
            else:
                self.dados =planilha
                
             # Remove valores vazios ou nulos
            if self.dados is not None:
                self.dados = self.dados.dropna()  # Remove linhas com valores NaN
                self.dados = self.dados.astype(str).str.strip()
                self.dados = self.dados[self.dados != ""]  # Remove valores vazios
                print(f"Dados carregados com sucesso! \n{self.dados}")
        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")

        return self.dados
    
def main():
    SS = inf_planilha("IA\\SOD\\excel\\rejeitar_ss.xlsx")
    start = SOD()
    lista_ss = SS.carregar_dados("SS")
    x=0
    for ss in lista_ss:
        print(x , ss, start.hora_atual())
        x=x+1



if __name__ =="__main__":
    main()

