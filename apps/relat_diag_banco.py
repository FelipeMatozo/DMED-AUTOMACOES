from datetime import datetime, timedelta
import os  # Para lidar com caminhos de arquivos e diretórios
import pandas as pd  # Para manipulação de dados tabulares
from selenium import webdriver  # Para automação de navegador web
from selenium.webdriver.common.by import By  # Para localizar elementos na página web
from selenium.webdriver.firefox.options import Options  # Opções do navegador Firefox
from time import sleep  # Para adicionar pausas no código
import zipfile  # Para trabalhar com arquivos ZIP
from selenium.webdriver.support.ui import WebDriverWait  # Para esperar até que certas condições sejam atendidas no navegador
from selenium.webdriver.support import expected_conditions as EC  # Condições esperadas pelo WebDriverWait
import schedule  # Para agendar a execução de tarefas em intervalos regulares de tempo
import time  # Para lidar com o tempo
import csv

def job():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("***********************************************************************************************\n")
    print(f"Horario de inicialização do macro: {agora}\n")
    print(f"INICIALIZANDO ATUALIZAÇÃO DE: -relatorio de diagnostico de telemetria.csv\n")

    pasta_download = os.path.dirname(__file__)
    pasta_output = os.path.join(pasta_download, '..', '..', '..')

    print(f"diretorio atual: {pasta_download} \n")
    print(f"diretorio saida: {pasta_output}\n ")

    print("***********************************************************************************************")
    abrir_hemera(pasta_download)

    puxar_arquivo_pasta(pasta_download, pasta_output)

    print(f"Será executado em 1 hora.\n")

def abrir_hemera(pasta_download):

 
    driver = webdriver.Firefox()
    driver.execute_script("window.open()")

    handles = driver.window_handles
    driver.get("https://operacao.ccee.org.br/ui/scde/cadastro/pontosmapeados")

    campo_login = driver.find_element(By.NAME, "username")
    campo_login.clear()
    campo_login.send_keys(login)

    campo_senha = driver.find_element(By.NAME, "password")
    campo_senha.clear()
    campo_senha.send_keys(senha)

    botao_login = driver.find_element(By.ID, "divCenterButton")
    botao_login.click()
    print("logado")
    sleep(3)
    driver.execute_script("window.open()")
    # Obter as alças (handles) das abas abertas
    handles = driver.window_handles
    # Mudar para a nova aba
    driver.switch_to.window(handles[2])
    # Abrir uma URL na nova aba

job()
schedule.every().hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
