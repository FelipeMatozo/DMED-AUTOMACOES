import subprocess
from time import sleep
from IA.ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import pyperclip
import os
import sys
from IA.banco_utils import add_banco  # Atualizado para importar banco_utils
import sqlite3

class consultaIris():
    
    def __init__(self):
        self.ia = Reconhecimento(numeroDeTentativasMax=15, delay=0.2)
        self.valorEncontrado = ''

    def consultarUC(self,numeroDaUC,numero_de_tms):
        programa = programasExecutaveis()
        programa.abrir()
        print(numeroDaUC)
        self.ia.cliqueDuplo('Conectar.png',0.8)
        self.ia.localiza('bt_listagem_telemetria.PNG', 0.7)
        self.ia.localiza('Config.PNG', 0.7)
        self.ia.localiza('Config_Bot_cobertura.PNG', 0.6)
        py.hotkey('down')
        py.hotkey('down')
        self.ia.localiza('bt_confirmar.PNG', 0.7)
        py.hotkey('enter')
        self.ia.localiza('tl_listagem_telemetrias.png', 0.65)
        py.click(py.moveRel(372,-174))
        self.ia.localiza('barra.png', 0.6)
        py.click(py.moveRel(30,15))
        py.write(numeroDaUC)
        py.hotkey('enter')
        self.ia.localiza('nome.png', 0.65)
        py.hotkey('ctrl', 'a')
        py.hotkey('ctrl', 'c')

        programa.fechar()

        self.valorEncontrado = pyperclip.paste()
        print(self.valorEncontrado)

        return self.valorEncontrado
    
    def tratar_input(self, dados):
        """
        Recebe uma lista de dados e retorna uma string com os dados separados por ponto e vírgula.
        
        Parâmetros:
        dados (list): Lista de strings ou inteiros representando os dados de entrada.
        
        Retorno:
        str: Dados separados por ";".
        """
        dados_limpos = [str(dado).strip() for dado in dados]
        return ';'.join(dados_limpos)

       
class programasExecutaveis():

    def __init__(self):
        self.caminho_iris = r"C:\Users\e805958\Downloads\Iris Manager\iris-manager.exe"
        # self.caminho_iris = r"C:\Program Files (x86)\CAS\Iris Manager\iris-manager.exe"
        self.processo = None  # Armazena a referência ao processo
        self.pid = ""
        
    def abrir(self):
        self.processo = subprocess.Popen(self.caminho_iris)
        self.pid = self.processo.pid
        print(f"Iris Manager iniciado com PID {self.processo.pid}")


    def fechar(self):
        py.click(1900,5)
        sleep(0.2)
        py.click(1900,5)

class Telemetria:
    def __init__(self, dados, caminho_banco):
        self.dados = dados
        self.caminho_banco = caminho_banco
        self.informacoes = []

    def processar_dados(self):
        """
        Processa os dados de entrada e armazena como dicionários em uma lista.
        """
        linhas = self.dados.strip().split('\n')
        for linha in linhas:
            valores = linha.split('\t')
            if len(valores) >= 5:  # Certifica-se de que existam pelo menos 5 valores
                codigo_tm = valores[0]
                numero_chip = valores[1]
                codigo_ponto = valores[2]
                operadora = valores[3]
                porta_tm = valores[4]
                self.informacoes.append({
                    'codigo_tm': codigo_tm,
                    'numero_chip': numero_chip,
                    'codigo_ponto': codigo_ponto,
                    'operadora': operadora,
                    'porta_tm': porta_tm
                })
            else:
                print(f"Erro: linha com número insuficiente de colunas - {valores}")


    def add_banco(self):
        """
        Adiciona as informações de telemetria processadas ao banco de dados utilizando banco_utils.
        """
        for info in self.informacoes:
            colunas = ["codigo_tm", "numero_chip", "codigo_ponto", "operadora", "porta_tm"]
            codigo_tm_com_prefixo = info['codigo_tm']
            valores = (codigo_tm_com_prefixo, info['numero_chip'], info['codigo_ponto'], info['operadora'], info['porta_tm'])
            add_banco("IRIS", colunas, valores)

def find_tm(telemetrias):

    programa = consultaIris()
    telemetrias_lista = telemetrias.split()
    numero_de_tms = len(telemetrias_lista)
    tele_string = programa.tratar_input(telemetrias_lista)
    dados = programa.consultarUC(tele_string, numero_de_tms)

    print(tele_string)

    # Defina o caminho para o banco de dados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(script_dir, '..', 'banco', 'banco_dmed.db')

    # Inicializa a classe e insere os dados no banco
    telemetria = Telemetria(dados, caminho_banco)
    telemetria.processar_dados()
    telemetria.add_banco()
    return telemetrias_lista
