import csv
import subprocess
from time import sleep
from IA.ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import sys
import os
import logging
from datetime import datetime
import keyboard

class CriarT:
    def __init__(self,SS, motivo, obs):
        self.ia = Reconhecimento(numeroDeTentativasMax=5, delay=0.9)
        self.arquivo = ''
        self.SS = SS
        self.motivo = motivo
        self.obs = obs

    def abrir_tela_servicos(self, Solicitacao):
        self.ia.online=True
        self.ia.localiza('telaInicial.PNG', 0.5)
        py.hotkey('alt','l')
        self.ia.localiza('SS.PNG', 0.85)
        py.write('01')
        py.hotkey('tab')
        py.write(f'{Solicitacao}')
        py.press('enter')
        sleep(2)

    def finalizacao(self):
        py.hotkey('alt','a')
        self.ia.verifica('comunicar_cliente.png',0.7)
        py.hotkey('alt','s')
        sleep(1)
        self.ia.verifica('comunicado_cliente.png',0.7)
        py.hotkey('space')
        sleep(0.5)
        py.hotkey('alt','o')
        sleep(1)
        self.ia.verifica('sonda_t11.png',0.7)
        py.hotkey('alt','o')
        sleep(1.5)
        self.ia.localiza('portinha.png',0.7)
        sleep(1.5)
        if self.ia.localiza('telaInicial.PNG', 0.5):
            pass
    
    def voltar_inicio(self):
        self.ia.online = True
        while self.ia.localiza_1x('telainicial.png', 0.5)== False:
            sleep(1.5)
            self.ia.localiza_1x('portinha.png', 0.7)

    def popupservico(self):

        print('Procurando popup')
        self.ia.popup()
        self.ia.online = True
            
    
    def consulta_ss(self):
        print("tentando localizar Consulta SS")
        self.ia.localiza('Consulta_SS.PNG', 0.6)
        py.click()
        sleep(2)
        self.ia.localiza('Acompanhamento_SS.png', 0.7)
        sleep(0.3)
        py.hotkey('alt','b')
        sleep(2)
        self.ia.localiza('Visto_verde.png', 0.7)
    

    def data_e_hora(self):
        # Obter a data e hora atual
        agora = datetime.now()
        print(f"Data e hora: {agora}")
        # Formatar a data e hora no formato desejado
        formato = agora.strftime("%d%m%Y%H%M")
        py.write(formato)

        
    def tabzon(self, numerodetabs):
        for tabs in range(numerodetabs):
            sleep(0.3)
            py.hotkey('tab')

class conclusao_ss:
    
    def tabzon(self, numerodetabs):

        for tabs in range(numerodetabs):
            py.hotkey('tab')

# Variável global para controlar a pausa
paused = False

def pause_program():
    global paused
    while True:
        if keyboard.is_pressed('p'):  # Altere 'p' para a tecla que você deseja usar
            paused = not paused  # Alterna entre pausar e retomar
            print("Programa pausado!" if paused else "Programa retomado!")
            sleep(1)  # Para evitar múltiplas ativações rápidas

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

    cis = CriarT(SS, motivo, obs)
    ia = Reconhecimento(numeroDeTentativasMax=5, delay=1)

    for Solicitacao in SS:
        sucesso = False
        while not sucesso:
            try:
                print(Solicitacao + '\n')

                # Verifica se o programa está pausado
                while paused:
                    sleep(0.5)  # Espera enquanto o programa está pausado

                # Executa suas funções aqui
                cis.abrir_tela_servicos(Solicitacao)
                try:
                    cis.popupservico()
                except Exception as e:
                    logging.warning(f"Popup não encontrado para UC: {Solicitacao}. Detalhes: {e}")

                cis.consulta_ss()

                if ia.verifica('cadas_reclam.png', 0.55):
                    print("Tela de Cadastro de Reclamação encontrada")
                    py.write(obs)
                    sleep(1)
                    cis.tabzon(2)
                    py.write(motivo)
                    cis.tabzon(4)
                    cis.data_e_hora()
                    cis.finalizacao()
                
                else:
                    # Se 'cadas_reclam.png' não for localizada, reinicia o loop
                    logging.warning(f"SS: {Solicitacao}. Retentando...")
                    cis.voltar_inicio()
                    continue


                if ia.localiza('telaInicial.PNG', 0.5):
                    sucesso = True
                    sleep(1)
                    logging.info(f"SS: {SS} finalizada! Servico: T12 Macro: Conclusao")
                else:
                    logging.warning(f"Tela inicial não encontrada para UC: {Solicitacao}. Retentando...")
                    cis.voltar_inicio()
                    continue

            except Exception as e:
                logging.error(f"Erro ao processar SS: {Solicitacao}. Detalhes: {e}")
                print(f"Erro ao processar SS: {Solicitacao}. Retentando...")