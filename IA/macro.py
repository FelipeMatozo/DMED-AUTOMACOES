import csv
import subprocess
from time import sleep
from IA.ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import sys
import os
import logging

class CriarT:
    def __init__(self):
        self.ia = Reconhecimento(numeroDeTentativasMax=7, delay=0.8)
        self.arquivo = ''

    def abrir_tela_servicos(self, unidade_consumidora):
        self.ia.localiza('telaInicial.PNG', 0.5)
        py.hotkey('alt','l')
        self.ia.localiza('uc.PNG', 0.7)   
        py.write(f'{unidade_consumidora}')
        py.press('enter')

    def popupservico(self):
        print('Procurando popup')
        self.ia.popup()
        
    def popupservico2(self):
        self.ia.online = True
        self.ia.localiza("popup2.png", 0.6)
        py.hotkey('alt','i')
        sleep(0.8)

    def inserir_reclama(self):
        self.ia.online = True
        print('insirindo parametro')
        self.ia.localiza('reclama.PNG', 0.8)
        py.move(0,+30)
        py.tripleClick()
        py.hotkey("backspace")
        py.write('SR/Reclama')
        py.hotkey("enter")
        py.hotkey("enter")

class ProgramasExecutaveis:
    def __init__(self):
        self.caminho_iris = r"C:\Program Files (x86)\Landis+Gyr\PLA-WIN\4.00.17\PadWin3.exe"
        self.processo = None  # Armazena a referência ao processo
        self.pid = ""
        self.dados_csv = []

    def abrir(self):
        self.processo = subprocess.Popen(self.caminho_iris)
        self.pid = self.processo.pid
        print(f"Iris Manager iniciado com PID {self.processo.pid}")

    def fechar(self):
        # Fecha o processo verificando cada processo ativo e comparando o caminho executável
        py.click(1900, 5)
        sleep(0.2)
        py.click(1900, 5)

    def importar_csv(self):
        current_dir = os.path.dirname(__file__)
        caminho_csv = os.path.join(current_dir, '..', 'assets', 'input.csv')
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            leitor = csv.reader(csvfile)
            self.dados_csv = [linha[0] for linha in leitor]
        print(f"Dados importados de {caminho_csv} com sucesso")
        return self.dados_csv

class CadastroSolicitacao:
    def __init__(self, ucs, subtipo, motivo, resp, obs):
        self.ia = Reconhecimento(numeroDeTentativasMax=7, delay=0.2)
        self.ucs= ucs
        self.subtipo = subtipo
        self.motivo = motivo
        self.resp = resp
        self.obs = obs
        self.email = 'sem-email@copel.com'

    def bloqueio_fatura(self):
        if self.ia.inf('bloqueio_de_faturas.png',0.7):
            sleep(0.8)
            py.hotkey('alt','n')
            sleep(0.3)
    
    def operacao_med(self, unidade_consumidora, subtipo):
        if self.ia.inf('oper_med.png', 0.65):
            py.hotkey('alt','o')
            self.ia.localiza('confirmar_area.png',0.8)
            py.hotkey('alt','s')
            py.press('enter')
            sleep(1)
        if self.ia.inf('ordem.png',0.8):
            sleep(1)
            py.hotkey('alt','o')        
            logging.info(f"UC: {unidade_consumidora} finalizada! Servico: {subtipo} Macro: Geracao")

        self.ia.localiza('sonda.png',0.6)
        py.hotkey('alt','o')
        if self.ia.localiza('telaInicial.PNG', 0.6):
            pass
        
    def tabzon(self, numerodetabs):
        for tabs in range(numerodetabs):
            py.hotkey('tab')
    
    def voltar_inicio(self):
        while self.ia.localiza_1x('telainicial.png', 0.5)== False:
            sleep(1.5)
            self.ia.localiza_1x('portinha.png', 0.7)
            sleep(1.5)
            if self.ia.localiza_1x('cancela_op.png', 0.7) == True:
                print("Cancelando operacao")
                py.hotkey('alt','s')
            sleep(1.5)
            if self.ia.localiza_1x('sonda_cancelada.png', 0.7) == True:
                print("Cancelando sonda")
                py.hotkey('alt','o')

    def inserir_email_T11(self):
        if self.ia.verifica('email.png',0.7):
            print("alt f")
            sleep(1.5)
            py.hotkey('alt','f')
            self.bloqueio_fatura()
            print("alt f")
            py.hotkey('alt','f')
            self.bloqueio_fatura()
            py.hotkey('alt','f')
            sleep(1.5)
            
        
        if self.ia.inf('gerar_os.png', 0.7):
            py.hotkey('alt','s')

    def inserir_obs(self):
        py.write(self.obs)
        py.hotkey('alt','f')
        sleep(1.5)
        self.bloqueio_fatura()
    
    def Interno(self): #INT
        self.ia.online = True
        self.tabzon(3)
        py.write(self.resp)
        self.tabzon(6)
        py.write(self.motivo)
        py.hotkey('tab')
        py.hotkey('shift','tab')
        py.write(self.subtipo)
        self.tabzon(5)
        self.inserir_obs()
        self.operacao_med()

    def Solicita(self,unidade_consumidora, subtipo): #SOL
        self.ia.online = True
        self.tabzon(3)
        py.write(self.resp)
        self.tabzon(6)
        py.write(self.motivo)
        self.tabzon(3)
        py.write(self.motivo)
        py.hotkey("tab")
        py.hotkey("shift", "tab")
        py.write(self.subtipo)
        self.tabzon(5)
        self.inserir_obs()
        self.inserir_email_T11()
        self.operacao_med(unidade_consumidora, subtipo)
        

def main(ucs, subtipo, motivo, resp, obs):
    # Remove espaços desnecessários e limpa a lista
    ucs = [uc.strip() for uc in ucs if uc.strip()]
    if ucs and ucs[-1] == '1':  # Remove UC de controle (opcional)
        ucs.pop()

    # Configuração de logging
    base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
    log_dir = os.path.join(base_path, 'assets', 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log = os.path.join(log_dir, 'log.log')
    logging.basicConfig(filename=log, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)

    cadastro = CadastroSolicitacao(ucs, subtipo, motivo, resp, obs)
    cis = CriarT()
    ia = Reconhecimento(numeroDeTentativasMax=7, delay=1)

    # Controle de processamento (garantir execução única)
    lista_processada = False  # Marca quando a lista foi concluída

    for unidade_consumidora in ucs:
        sucesso = False
        while not sucesso:
            try:
                print(f"Processando UC: {unidade_consumidora}")
                # Chamadas principais do processo
                cis.abrir_tela_servicos(unidade_consumidora)
                sleep(2)
                cis.popupservico()
                cis.inserir_reclama()
                cis.popupservico2()
                sleep(1)
                cis.popupservico()

                # Verifica tela de cadastro e inicia solicitação
                if ia.verifica('cadas_reclam.png', 0.5):
                    print("Tela de Cadastro de Reclamação encontrada")
                    cadastro.Solicita(unidade_consumidora, subtipo)
                else:
                    logging.warning(f"UC: {unidade_consumidora}. Retentando...")
                    cadastro.voltar_inicio()
                    continue  # Reinicia o loop para essa UC específica

                # Verifica se voltou à tela inicial
                if ia.localiza('telaInicial.PNG', 0.5):
                    logging.info(f"UC: {unidade_consumidora} finalizada! Serviço: {subtipo}")
                    sucesso = True  # Finaliza o loop desta UC
                else:
                    logging.warning(f"Verificar geração: {unidade_consumidora}.")
                    cadastro.voltar_inicio()
                    sucesso = True

            except Exception as e:
                logging.error(f"Erro ao processar UC: {unidade_consumidora}. Detalhes: {e}")
                print(f"Erro ao processar UC: {unidade_consumidora}. Retentando...")

    # Marca lista como processada
    lista_processada = True

    # Garante que o loop não reinicie
    if lista_processada:
        print("Processamento de todas as UCs concluído com sucesso.")
        return "Processamento concluído"  # Retorna ao Flask
