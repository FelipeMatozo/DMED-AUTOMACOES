import os
import sys
import logging
import pandas as pd
from time import sleep
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as py
import pyperclip
import keyboard

# Adicione o diretório base ao sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, base_dir)
from IA.ReconhecimentoDeImagem import Reconhecimento

class GerenciadorPlanilha:
    """Gerencia a criação e salvamento da planilha com os dados coletados"""
    def __init__(self, caminho_planilha):
        self.caminho_planilha = caminho_planilha
        self.dados = pd.DataFrame(columns=["CODIGO PM", "NOME", "TIPO DE COLETA", "STATUS", "INICIO VIGENCIA","DATA STATUS","COMENTARIO"
])
    
    def salvar_planilha(self):
        """Salva os dados na planilha"""
        self.dados.to_excel(self.caminho_planilha, index=False)
    
    def adicionar_dado(self, nome, codigo, tipo_coleta, status ,inicio_vigencia, data_status, comentario):
        """Adiciona uma nova linha na planilha"""
        nova_linha = pd.DataFrame([{  # Substitui append pelo método correto
            "CODIGO PM": codigo,
            "NOME": nome,
            "TIPO DE COLETA": tipo_coleta,
            "INICIO VIGENCIA": inicio_vigencia,
            "STATUS": status,
            "DATA STATUS": data_status,
            "COMENTARIO": comentario,
        }])
        
        self.dados = pd.concat([self.dados, nova_linha], ignore_index=True)
        self.salvar_planilha()

class ProcessadorPM:
    """Classe responsável por buscar os dados das PMs no site"""
    def __init__(self, caminho_planilha):
        self.planilha = GerenciadorPlanilha(caminho_planilha)
        self.configurar_logging()
        self.ia = Reconhecimento(numeroDeTentativasMax=5, delay=0.9)
    
    def configurar_logging(self):
        log_path = os.path.join(base_dir, 'assets', 'log', 'log_relatorio_uc.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        logging.basicConfig(
            filename=log_path,
            filemode='a',
            format='%(asctime)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S',
            level=logging.INFO
        )
    
    def tela_inicio(self):
        self.ia.verifica_ccee("tela_inicio.png", 0.65)
        py.scroll(-1300)
        self.ia.localiza_ccee("ponto_medicao.png", 0.65)
        return True
    
    def inf_cod(self):
        self.ia.localiza_ccee("parte_cod.png", 0.7)
        py.moveRel(0,40)
        py.doubleClick()
        py.mouseDown()
        py.moveRel(1700,0)
        py.mouseUp()
       
        py.hotkey("ctrl", "c")
        inf_pm = pyperclip.paste()
        return inf_pm
    
    def tratar_inf_cod(self, inf_pm):
        """Processa os dados extraídos e retorna os valores formatados."""
        partes = inf_pm.split("\t")  # Divide pelo tabulador
        if len(partes) >= 4:
            codigo = partes[0]
            tipo_coleta = partes[1]
            status = partes[3]
            return codigo, tipo_coleta, status
        else:
            logging.error("Erro ao processar inf_pm: formato inesperado")
            return None, None, None
        
    def edit_pm(self):
        self.ia.localiza_ccee("nome.png", 0.8)

        py.moveRel(0,30)
        sleep(0.5)
        py.click()
        py.click()
        py.click()

        py.hotkey("ctrl", "c")
        nome = pyperclip.paste()

        
        self.ia.localiza_ccee("inicio_vigencia.png", 0.8)

        py.moveRel(0,30)
        sleep(0.5)
        py.click()
        py.click()
        py.click()

        py.hotkey("ctrl", "c")
        inicio_vigencia = pyperclip.paste()

        py.scroll(-1800)

        self.ia.localiza_ccee("historico_cadastro.png", 0.75)
        py.moveRel(-105,0)
        py.click()

        py.scroll(-400)

        self.ia.localiza_ccee("data_status.png", 0.75)
        py.moveRel(0,30)
        py.tripleClick()
        py.hotkey("ctrl", "c")
        data_status = pyperclip.paste()

        self.ia.localiza_ccee("comentario.png", 0.75)
        py.moveRel(0,30)
        py.tripleClick()
        py.hotkey("ctrl", "c")
        comentario = pyperclip.paste()

        self.ia.localiza_ccee("voltar.png", 0.75)
        sleep(1.5)
        py.hotkey("f5")

        return nome, inicio_vigencia, data_status, comentario

    def buscar_dados_pm(self, pm):

        self.ia.localiza_ccee("tipo_agente.png", 0.65)
        py.hotkey("down")
        py.hotkey("enter")
        py.hotkey("tab")
        if not isinstance(pm, str):
            pm = str(pm)  # Converte para string se necessário
        py.write(pm) 
        sleep(2)
        py.moveRel(1350,50)
        py.click()
        self.ia.localiza_ccee("pesquisar.png", 0.65)
       
        logging.info(f"Buscando dados para PM: {pm}")
        inf_pm = self.inf_cod()
        codigo, tipo_coleta, status= self. tratar_inf_cod(inf_pm)
        self.ia.localiza_ccee("entrar_pm.png", 0.7)
        nome, inicio_vigencia, data_status, comentario =self.edit_pm()
        print(nome)
        print(codigo)
        print(tipo_coleta)
        print(status)
        print(inicio_vigencia)
        print(data_status)
        print(comentario)

        return nome, codigo, tipo_coleta, status, inicio_vigencia, data_status, comentario
    
    
    def processar_pms(self, lista_pms):
        """Percorre todas as PMs fornecidas e busca seus dados"""
        self.tela_inicio()
        for pm in lista_pms:
            try:
                print(f"{pm} primeiro")
                dados_pm = self.buscar_dados_pm(pm)
                self.planilha.adicionar_dado(*dados_pm)
            except Exception as e:
                logging.error(f"Erro ao processar PM {pm}: {e}")
                print(f"Erro ao processar Ponto {pm}: {e}")
def start(lista_pms):
    caminho_planilha = os.path.join(base_dir, 'assets', 'excel', 'dados_pms.xlsx')
    print(caminho_planilha)
    processador = ProcessadorPM(caminho_planilha)
    processador.processar_pms(lista_pms)

if __name__ == "__main__":
    start(lista_pms=[""])