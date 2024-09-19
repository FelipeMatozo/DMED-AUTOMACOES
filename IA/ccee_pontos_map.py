# import csv
# import subprocess
from time import sleep
# from ReconhecimentoDeImagem import Reconhecimento
# import pyautogui as py
# import sys
# import os
# import logging
# import selenium
# 47948884
from playwright.sync_api import sync_playwright

def run(playwright):
    # Inicializa o navegador
    browser = playwright.chromium.launch(headless=False)  # Modo headless=False abre o navegador visivelmente
    context = browser.new_context()

    # Abre uma nova página
    page = context.new_page()

    # Navega até a URL desejada
    page.goto("https://operacao.ccee.org.br/ui/scde/cadastro/pontosmapeados")
    sleep(10000)
    # Insere dados no formulário
    page.fill("input#nome", "Seu Nome")
    page.fill("input#email", "seuemail@example.com")

    # Submete o formulário
    page.click("button#submit")  # Assumindo que o botão de envio tem o ID "submit"

    # Pode adicionar uma pausa para observar o resultado
    
    sleep(10000)
    # Fecha o navegador
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
