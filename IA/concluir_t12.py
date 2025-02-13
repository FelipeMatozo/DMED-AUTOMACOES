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
    def __init__(self, SS, motivo, obs):
        """
        Inicializa a classe CriarT com as variáveis SS (serviços), motivo e observações.
        Configura também o reconhecimento de imagem e outras variáveis de controle.
        """
        self.ia = Reconhecimento(numeroDeTentativasMax=5, delay=0.9)
        self.arquivo = ''
        self.SS = SS
        self.motivo = motivo
        self.obs = obs

    def abrir_tela_servicos(self, Solicitacao):
        """
        Abre a tela de serviços para o SS fornecido.
        Localiza a tela inicial e a tela do SS, e preenche os campos necessários.
        """
        self.ia.online=True
        self.ia.localiza('telaInicial.PNG', 0.5)
        py.hotkey('alt','l')
        self.ia.localiza('SS.PNG', 0.85)
        py.write('01')
        py.hotkey('tab')
        py.write(f'{Solicitacao}')
        py.press('enter')
        sleep(2)

    def finalizacao(self, SS):
        """
        Finaliza o serviço SS, comunicando o cliente e verificando a conclusão.
        Verifica se a tela final de comunicação é encontrada e realiza as ações necessárias.
        """
        sleep(1)
        py.hotkey('alt','a')
        self.ia.verifica('comunicar_cliente.png', 0.7)
        py.hotkey('alt','s')
        sleep(1)
        self.ia.verifica('comunicado_cliente.png', 0.7)
        py.hotkey('space')
        sleep(0.5)
        py.hotkey('alt','o')
        sleep(1)
        if self.ia.verifica('sonda_t11.png',0.65):
            py.hotkey('alt','o')
            logging.info(f"SS: {SS} finalizada! Servico: T12 Macro: Conclusao")
        else:
            logging.info(f"Verificar SS: {SS} Servico: T12 Macro: Conclusao")
        sleep(1.5)
        self.ia.localiza('portinha.png',0.7)
        sleep(1.5)
        if self.ia.localiza('telaInicial.PNG', 0.5):
            pass
    
    def voltar_inicio(self):
        """
        Retorna à tela inicial do processo, aguardando que a tela inicial seja localizada.
        """
        self.ia.online = True
        while self.ia.localiza_1x('telainicial.png', 0.5)== False:
            sleep(1.5)
            self.ia.localiza_1x('portinha.png', 0.7)

    def popupservico(self):
        """
        Procura e interage com o popup de serviço.
        """
        print('Procurando popup')
        self.ia.popup()
        self.ia.online = True
            
    def consulta_ss(self):
        """
        Realiza a consulta SS, localizando a tela de consulta e verificando os status.
        """
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
        """
        Obtém a data e hora atual e escreve no formato desejado.
        """
        # Obter a data e hora atual
        agora = datetime.now()
        print(f"Data e hora: {agora}")
        # Formatar a data e hora no formato desejado
        formato = agora.strftime("%d%m%Y%H%M")
        print(formato)
        py.write(formato)

    def tabzon(self, numerodetabs):
        """
        Realiza um número específico de pressionamentos da tecla TAB.
        """
        for tabs in range(numerodetabs):
            sleep(0.3)
            py.hotkey('tab')

class conclusao_ss:
    
    def tabzon(self, numerodetabs):
        """
        Realiza um número específico de pressionamentos da tecla TAB.
        """
        for tabs in range(numerodetabs):
            py.hotkey('tab')

# Variável global para controlar a pausa
paused = False

def pause_program():
    """
    Pausa o programa quando a tecla 'p' é pressionada. Alterna entre pausar e retomar a execução.
    """
    global paused
    while True:
        if keyboard.is_pressed('p'):  # Altere 'p' para a tecla que você deseja usar
            paused = not paused  # Alterna entre pausar e retomar
            print("Programa pausado!" if paused else "Programa retomado!")
            sleep(1)  # Para evitar múltiplas ativações rápidas

def main(SS, motivo, obs):
    """
    Função principal que coordena a execução do processo de finalização de serviços.
    Realiza a interação com a interface, realiza a consulta SS, e trata a tela de reclamação.
    """
    print("iniciando Conclusao T12")
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
    ia = Reconhecimento(numeroDeTentativasMax=7, delay=1)
     # Controle de processamento (garantir execução única)
    lista_processada = False  # Marca quando a lista foi concluída
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
                    cis.finalizacao(Solicitacao)
                
                else:
                    # Se 'cadas_reclam.png' não for localizada, reinicia o loop
                    logging.warning(f"SS: {Solicitacao}. Retentando...")
                    cis.voltar_inicio()
                    continue


                if ia.localiza('telaInicial.PNG', 0.5):
                    sucesso = True
                    sleep(1)
                else:
                    logging.warning(f"Verificar conclusao: {Solicitacao}")
                    cis.voltar_inicio()
                    sucesso = True

            except Exception as e:
                logging.error(f"Erro ao processar SS: {Solicitacao}. Detalhes: {e}")
                print(f"Erro ao processar SS: {Solicitacao}. Retentando...")
    
    # Marca lista como processada
    lista_processada = True

    # Garante que o loop não reinicie
    if lista_processada:
        print("Processamento de todas as UCs concluído com sucesso.")
        return "Processamento concluído"  # Retorna ao Flask
