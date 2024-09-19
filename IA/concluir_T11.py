import csv
import subprocess
from time import sleep
from IA.ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import sys
import os
import logging
from datetime import datetime

class CriarT:
    def __init__(self,SS, motivo, obs):
        self.ia = Reconhecimento(numeroDeTentativasMax=5, delay=0.5)
        self.arquivo = ''
        self.SS = SS
        self.motivo = motivo
        self.obs = obs

    def abrir_tela_servicos(self, Solicitacao):
        self.ia.localiza('telaInicial.PNG', 0.6)
        py.hotkey('alt','l')
        self.ia.localiza('SS.PNG', 0.85)
        py.write('01')
        py.hotkey('tab')
        py.write(f'{Solicitacao}')
        py.press('enter')

    def finalizacao(self):
        py.hotkey('alt','a')
        self.ia.verifica('comunicar_cliente.png',0.7)
        py.hotkey('alt','s')
        self.ia.verifica('comunicado_cliente.png',0.7)
        py.hotkey('space')
        py.hotkey('alt','o')
        self.ia.verifica('sonda_t11.png',0.7)
        py.hotkey('alt','o')
        self.ia.localiza('portinha.png',0.7)


    def popupservico(self):
        print('Procurando popup')
        self.ia.popup()
    
    def consulta_ss(self):
        self.ia.localiza('Consulta_SS.PNG', 0.7)
        self.ia.localiza('Acompanhamento_SS.png', 0.7)
        py.hotkey('alt','b')
        sleep(2)
        self.ia.localiza('Visto_verde.png', 0.7)
        self.ia.verifica('cadas_reclam.png', 0.7)
        py.write(self.obs)
        sleep(1)

    def data_e_hora(self):
        # Obter a data e hora atual
        agora = datetime.now()
        print(f"Data e hora: {agora}")
        # Formatar a data e hora no formato desejado
        formato = agora.strftime("%d%m%Y%H%M")
        py.write(formato)

        
    def tabzon(self, numerodetabs):
        for tabs in range(numerodetabs):
            py.hotkey('tab')

class conclusao_ss:
    
    def tabzon(self, numerodetabs):

        for tabs in range(numerodetabs):
            py.hotkey('tab')

def main(SS, motivo, obs):

    SS = [servico.replace('\r', '').replace('\n', '').strip() for servico in SS if servico.replace('\r', '').replace('\n', '').strip()]
    print(SS, motivo, obs)
     # Verifica se estamos em um ambiente PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Caminho para o diretório de log
    log_dir = os.path.join(base_path, 'assets', 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Caminho completo para o arquivo de log
    log = os.path.join(log_dir, 'log.log')
    logging.basicConfig(filename=log, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
    conclusao = conclusao_ss()
    logging.info(f"Rodando SS's: {SS}")
    logging.info(f"Configuracao:  {motivo}")
    logging.info(f"Observacao: {obs}")

    cis = CriarT(SS, motivo, obs)
    ia = Reconhecimento()

    for Solicitacao in SS:
        print(Solicitacao + '\n')
        cis.abrir_tela_servicos(Solicitacao)
        cis.popupservico()
        cis.consulta_ss()
        cis.tabzon(2)
        py.write(motivo)
        cis.tabzon(4)
        cis.data_e_hora()
        cis.finalizacao()
        
        



        logging.info(f"UC: {Solicitacao} finalizada!")