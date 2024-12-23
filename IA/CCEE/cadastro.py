from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import sys
import os
# Adicione o diretório base ao sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, base_dir)
from IA.ReconhecimentoDeImagem import Reconhecimento
import unicodedata
import re
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui as py
import pyperclip
import sys
import math
import os
import logging
from datetime import datetime, timedelta
import keyboard
from time import sleep



# class page_ccee:
#     def __init__(self, url):
#         self.path_ccee = url
#         self.driver = None

#     def entrar_ccee(self, continuar_evento, usuario, senha):
#         options = Options()
#         self.driver = webdriver.Firefox(options=options)
#         self.driver.get(self.path_ccee)
        
#         print(usuario)
#         wait = WebDriverWait(self.driver, 10)
#         # Localiza os campos de entrada de login e senha
#         username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))  # Substitua pelo nome correto
#         password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))  # Substitua pelo nome correto

#         # Insere as credenciais
#         username_input.clear()
#         username_input.send_keys(usuario)
#         password_input.clear()
#         password_input.send_keys(senha)

#         # Clica no botão de login
#         login_button = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(text(), 'Entrar')]")
#             ))
#         login_button.click()
        
#         # Clica no botão de login
#         sms_button = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(text(), 'SMS')]")
#             ))
#         sms_button.click()

#         print("Esperando o login manual na interface Flask...")
#         continuar_evento.wait()  # Pausa aqui até que o evento seja ativado


#         print("Login confirmado. Continuando com o processo.")

#         # # Abrir uma nova guia e acessar a URL desejada
#         # self.driver.execute_script("window.open('https://operacao.ccee.org.br/ui/scde/cadastro/pontosdemedicao', '_blank');")
        
#         # # Alternar para a nova guia
#         # self.driver.switch_to.window(self.driver.window_handles[-1])
#         sleep(5)

#     def buscar_info_uc(self, info_uc):
#         """Método para buscar informações no site da CCEE para uma UC específica"""
#         # Exemplo de busca no site da CCEE usando informações da UC
#         pass

#     def encontra_pts_med(self, cod_ponto):
#         """Função para encontrar e clicar em 'Pontos de Medição' e inserir o 'cod_ponto' no campo apropriado"""
        
#         wait = WebDriverWait(self.driver, 10)

#         try:
#             # Localiza o link "Pontos de Medição" e clica
#             pontos_medicao_link = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//div[contains(@class, 'ng-tns-c31-149')]//a[contains(., 'Pontos de Medição')]")
#             ))
#             pontos_medicao_link.click()

#             # Aguarda o iframe estar disponível e muda o contexto para o iframe
#             iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://scde.ccee.org.br/ui/cadastro/pontos-medicao/pesquisa')]")))
#             self.driver.switch_to.frame(iframe)

#             # Adiciona uma pausa para garantir que o campo está carregado
#             time.sleep(2)  # Ajuste conforme necessário

#             # Aguarda o campo de entrada do código SCDE estar visível e insere o valor de 'cod_ponto'
#             cod_ponto_input = wait.until(EC.visibility_of_element_located(
#                 (By.XPATH, "//input[@name='gx-form-group-4']")
#             ))
#             cod_ponto_input.clear()  # Limpa o campo caso tenha algum valor pré-existente
#             cod_ponto_input.send_keys(cod_ponto)

#             print(f"Valor '{cod_ponto}' inserido no campo de código SCDE.")

#         except TimeoutException:
#             print("Elemento 'Pontos de Medição' ou campo de entrada do código SCDE não encontrado.")
#         except Exception as e:
#             print(f"Erro ao interagir com a página: {e}")
#         finally:
#             # Sempre que terminar, volte ao contexto principal (opcional)
#             self.driver.switch_to.default_content()

#     def seleciona_opcao(self, valor_opcao="601", valor_inclusao="1401"):
#         """Seleciona opções específicas em caixas de seleção na página."""
#         sleep(3)
#         wait = WebDriverWait(self.driver, 10)

        
        
#         try:
#             # Seleciona a primeira caixa de seleção
#             select_element = wait.until(EC.element_to_be_clickable(
#                 (By.NAME, "gx-form-group-2")
#             ))
#             select_element.click()

#             # Seleciona a opção "Medição" (valor_opcao) pelo valor
#             opcao = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//option[contains(text(), 'Medição')]")
#             ))
#             opcao.click()
#             print("Opção 'Medição' selecionada.")

#             # Seleciona a opção "Solic. Inclusão - cadastro" (valor_inclusao) pelo valor
#             opcao_inclusao = select_element.find_element(By.XPATH, f"//option[@value='{valor_inclusao}']")
#             opcao_inclusao.click()
#             print("Opção 'Solic. Inclusão - cadastro' selecionada.")

#         except TimeoutException:
#             print("Caixa de seleção não encontrada.")
#         except Exception as e:
#             print(f"Erro ao interagir com a caixa de seleção: {e}")

#     def clicar_pesquisar(self):

#         wait = WebDriverWait(self.driver, 10)
#         try:
#             # Aguarda o botão 'Pesquisar' estar visível e clica
#             pesquisar_btn = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(@class, 'btn-primary') and contains(., 'Pesquisar')]")
#             ))
#             pesquisar_btn.click()
#             print("Botão 'Pesquisar' clicado.")

#         except TimeoutException:
#             print("Botão 'Pesquisar' não encontrado.")
#         except Exception as e:
#             print(f"Erro ao interagir com o botão 'Pesquisar': {e}")

#     def clicar_solicitacoes(self):
#         """Clica no botão 'Solicitações' na página dentro de um iframe"""
#         wait = WebDriverWait(self.driver, 10)
#         try:
#             # Muda para o iframe que contém o botão
#             iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://scde.ccee.org.br/ui/cadastro/pontos-medicao/pesquisa')]")))
#             self.driver.switch_to.frame(iframe)

#             # Espera até que o botão esteja visível e clicável
#             solicitacoes_btn = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(text(), 'Solicitações')]")
#             ))
#             solicitacoes_btn.click()
#             print("Botão 'Solicitações' clicado.")

#             # Após clicar no botão, espera que o select apareça
#             self.seleciona_opcao()

#             # Retorna ao contexto principal, se necessário
#             self.driver.switch_to.default_content()

#         except TimeoutException:
#             print("Botão 'Solicitações' não encontrado.")
#         except Exception as e:
#             print(f"Erro ao interagir com o botão 'Solicitações': {e}")

#     def verificar_pesquisa(self):
#         """Verifica se o `span` de resultados está presente na página após a pesquisa."""
        
#         wait = WebDriverWait(self.driver, 10)
        
#         try:
#             # Aguarda a presença do span que indica resultados
#             span_resultado = wait.until(EC.presence_of_element_located(
#                 (By.XPATH, "//span[@ng-if='pontosMedicaoResultado && pontosMedicaoResultado.length']")
#             ))
#             print("Resultados encontrados.")
#             return True  # Span encontrado

#         except TimeoutException:
#             print("Resultados não encontrados.")
#             return False  # Span não encontrado

#     def novo_ponto_medicao(self):
#         """Clica no link 'Novo ponto de medição' se não houver resultados."""
        
#         wait = WebDriverWait(self.driver, 10)
        
#         try:
#             # Muda para o iframe
#             iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://scde.ccee.org.br/ui/cadastro/pontos-medicao/pesquisa')]")))
#             self.driver.switch_to.frame(iframe)

#             # Localiza e clica no botão de dropdown "Ações"
#             dropdown_btn = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[@data-toggle='dropdown' and contains(., 'Ações')]")
#             ))
#             dropdown_btn.click()  # Abre o dropdown
#             print("Dropdown 'Ações' clicado.")

#             # Aguarda um pouco para garantir que as opções do dropdown estejam visíveis     

#             sleep(1)  # Ajuste o tempo se necessário

#             # Localiza e clica no link 'Novo ponto de medição'
#             link_novo_ponto = wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//a[@ui-sref='root.cadastro.pontosMedicao.criacao.principal' and contains(., 'Novo ponto de medição')]")
#             ))
#             link_novo_ponto.click()
#             print("Clicou em 'Novo ponto de medição'.")

#         except TimeoutException:
#             print("Erro: O link 'Novo ponto de medição' ou o botão de dropdown não foi encontrado ou não está clicável.")
#         except Exception as e:
#             print(f"Ocorreu um erro: {e}")
#         finally:
#             # Sempre que terminar, volte ao contexto principal (opcional)
#             self.driver.switch_to.default_content()

#     def inserir_codigo_ponto(self, cod_ponto):
#         """Insere o código do ponto no campo de texto 'codigoMaePontoMapeado' e seleciona a opção correspondente no menu suspenso."""
        
#         wait = WebDriverWait(self.driver, 10)
        
#         try:
#             # Muda para o iframe onde o campo está localizado
#             iframe = wait.until(EC.presence_of_element_located(
#                 (By.XPATH, "//iframe[contains(@src, 'https://scde.ccee.org.br/ui/cadastro/pontos-medicao/pesquisa')]")
#             ))
#             self.driver.switch_to.frame(iframe)  # Muda o contexto para o iframe

#             # Localiza o campo de texto e insere o código do ponto
#             input_cod_ponto = wait.until(EC.presence_of_element_located(
#                 (By.NAME, "codigoMaePontoMapeado")
#             ))
#             input_cod_ponto.clear()  # Limpa o campo antes de inserir
#             input_cod_ponto.send_keys(cod_ponto)  # Insere o código
#             print(f"Código '{cod_ponto}' inserido no campo 'codigoMaePontoMapeado'.")

#             # Espera até que o menu suspenso esteja visível
#             menu_suspenso = wait.until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu"))
#             )
            
#             # Clica para abrir o menu suspenso (se necessário)
#             menu_suspenso.click()

#             # Espera até que as opções estejam disponíveis
#             opcoes = wait.until(
#                 EC.visibility_of_all_elements_located((By.XPATH, "//li/a[contains(@ng-click, '$ctrl.selectOption')]"))
#             )
            
#             # Procura pela opção desejada e clica nela
#             for opcao in opcoes:
#                 if cod_ponto in opcao.text:
#                     opcao.click()  # Clica na opção desejada
#                     print(f'Opção selecionada: {cod_ponto}')
#                     break
#             else:
#                 print(f'Opção "{cod_ponto}" não encontrada no menu.')

#         except TimeoutException:
#             print("Erro: O campo de texto 'codigoMaePontoMapeado' não foi encontrado ou está inacessível.")
#         except Exception as e:
#             print(f'Ocorreu um erro: {e}')
#         finally:
#             # Volta ao contexto principal (opcional)
#             self.driver.switch_to.default_content()
            
class inserir_inf:
    def __init__(self):
        self.ia = Reconhecimento(numeroDeTentativasMax=5, delay=0.9)
        # Diretório base do projeto (onde o script está localizado)
        self.diretorio_base = os.path.dirname(os.path.abspath(__file__),)
        self.PAUSE_FILE = os.path.join(os.path.dirname(os.path.dirname(self.diretorio_base)), 'assets', 'txt', 'pause.txt')
        self.caminho_log = os.path.join(os.path.dirname(os.path.dirname(self.diretorio_base)), 'assets', 'log', 'log_ccee.log')


    
    def start_cadastro(self):
        print("Iniciando cadastro")
        self.ia.verifica("inicio_cadastro.png", 0.7)
        # nome_curto = self.encurta_nome()
        self.inserir_apelido()
    
    def encurta_nome(self, nome):
        """Copia o texto do campo 'nomePontoMedicao', encurta pulando a primeira palavra e mantendo as duas próximas."""

        palavras = nome.split()  # Divide o texto em palavras

        # Pega a segunda e a terceira palavras, se houverem
        if len(palavras) > 2:
            texto_encurtado = " ".join(palavras[1:3])  # Pega as duas palavras seguintes
        else:
            texto_encurtado = " ".join(palavras[1:])  # Se houver menos de 3 palavras, pega até o final

        # Limita o texto encurtado a 15 caracteres
        if len(texto_encurtado) > 15:
            texto_encurtado = texto_encurtado[:15]  # Trunca o texto para 15 caracteres

        print(f'Texto encurtado do campo "nomePontoMedicao": "{texto_encurtado}"')
        return texto_encurtado
   
    def inserir_apelido(self):
        self.ia.verifica('nome_completo.png', 0.7)
        py.moveRel(0,+32)
        py.tripleClick()
        nome_completo = py.hotkey('ctrl','c')
        nome_completo = pyperclip.paste()
        print(nome_completo)
        apelido = self.encurta_nome(nome_completo)
        print(apelido)
        self.ia.localiza('nome_apelido.png', 0.7)
        sleep(0.2)
        py.write(apelido)
        sleep(1)

    def inserir_dados_pnt_med(self, ini_vig, cap_ger, cap_con):
        """Insere a data de conclusão de vigência e a capacidade nominal de geração no formulário."""
        self.tabzon(2)
        # Converter a data para o formato DD/MM/YYYY
        try:
            # Parse a string de data e hora
            data_original = datetime.strptime(ini_vig, "%Y-%m-%d %H:%M:%S")
            # Formatar para o formato desejado
            data_formatada = data_original.strftime("%d%m%Y")
            print(data_formatada)
        except ValueError:
            print("Erro: Data no formato inválido. Use 'YYYY-MM-DD HH:MM:SS'.")
            return  # Retorna se a data estiver em formato inválido
        
        py.write(data_formatada)
        self.tabzon(1)
        py.write(cap_ger)
        self.tabzon(1)
        py.write(cap_con)
        sleep(1)
        
    def ver_tcs(self, tc_a, tc_b, tc_c):
        """Verifica se as colunas TC_A, TC_B e TC_C estão preenchidas e conta o total."""
        preenchidos = 0

        def is_preenchido(valor):
            """Verifica se o valor é realmente preenchido"""
            if pd.isna(valor):  # Verifica explicitamente se é NaN
                return False
            if valor is None:  # Verifica se é None
                return False
            if isinstance(valor, str) and valor.strip() == "":  # Verifica strings vazias
                return False
            return True  # Caso contrário, está preenchido

        if is_preenchido(tc_a):
            preenchidos += 1
        if is_preenchido(tc_b):
            preenchidos += 1
        if is_preenchido(tc_c):
            preenchidos += 1

        print(f"Total preenchido: {preenchidos}")

        if(preenchidos==2):
            self.tabzon(1)
            py.hotkey('enter')
            self.tabzon(2)
            
        if(preenchidos==3):
            self.tabzon(2)
            py.hotkey('enter')
            self.tabzon(1)

        return preenchidos


    def localizacao(self, municipio):
        py.hotkey('enter')
        py.write("P")
        x = 0
        while(x<4):
            py.hotkey('down')
            x=x+1

        py.hotkey('enter')

        print(municipio)
        
        self.ia.localiza("cidade.png", 0.7)
        py.moveRel(0,-70)
        primeira_letra = municipio[0]
        py.write(primeira_letra)
        self.ia.localizar_palavra_rolando(municipio, max_tentativas=20, scroll_pixels=-175)
        self.tabzon(2)
        py.hotkey('enter')
        self.tabzon(2)
        py.write("https://coleta.ccee.copel.com.br/")
        self.tabzon(1)
        py.write("cliente")
        self.tabzon(1)
        py.write("cas")     
        self.tabzon(1)
        py.write("cliente")
        self.tabzon(1)
        py.write("cas")

        self.tabzon(3)
        py.hotkey('enter')
        py.hotkey('down')
        py.hotkey('enter')
        sleep(1)
        self.tabzon(1)
        py.write("COPEL DISTRIB")
        self.tabzon(1)
        py.hotkey('enter')
        sleep(0.5)
        py.scroll(-1000)
        sleep(1)
        self.ia.localiza("gravar.png", 0.8)
        sleep(0.5)
        py.click()
        sleep(20)
         
    def trans_corren(self, q_tcs, tc_a,tc_b,tc_c, rel_exis, tp_a):
        quantidade_tcs = q_tcs
        try:
            x, y = map(float, rel_exis.split('/'))  # Divide o string em dois valores e converte para float
            result = x / y  # Calcula a divisão
            # Verifica se o resultado é um número inteiro
            rel_uti = int(result) if result.is_integer() else result
            print(f"Relação utilizada (rel_uti): {rel_uti}")        

        except ValueError:      
            print("Erro: rel_exis não está no formato esperado 'x/y'")
            rel_uti = None  # Define como None caso o formato esteja errado

        def is_preenchido():
            """Verifica se o valor é realmente preenchido"""
            if pd.isna(tp_a):  # Verifica explicitamente se é NaN       

                return False
            if tp_a is None:  # Verifica se é None
                return False
            if isinstance(tp_a, str) and tp_a.strip() == "":  # Verifica strings vazias
                return False
            return True  # Caso contrário, está preenchido   

        

        q_tcs =str(q_tcs)
        self.ia.localiza("trans_corrente.png", 0.9)
        sleep(2)
        self.ia.localiza("q_transform.png", 0.7)
        py.write(q_tcs)
        py.hotkey('enter')
        n_tcs_rodados= 2        

        print(q_tcs, tc_a, tc_b,tc_c, rel_exis) 
    
        # Exibe os parâmetros recebidos e a relação utilizada       


                    
        rel_uti = str(rel_uti)
        tc_a = float(tc_a)
        tc_a = int(tc_a)
        tc_a = str(tc_a)

        tc_b = float(tc_b)
        tc_b = int(tc_b)
        tc_b = str(tc_b)        


        tc_c = float(tc_c)
        tc_c = int(tc_c)
        tc_c = str(tc_c)

        self.ia.localiza("novo_tc.png", 0.7)
        self.ia.localiza("numero_serie.png", 0.7)       

        py.doubleClick()        

        py.hotkey("del")
        
        py.write(tc_a)
         

        
        self.tabzon(1)
        py.write(rel_exis)
        self.tabzon(1)
        py.write(rel_uti)
        self.tabzon(3)      
        self.ia.localiza("exatidao.png", 0.6)
        py.moveRel(0,+35)
        valor_tp = is_preenchido()
        if valor_tp:     
            py.hotkey("down")       

        else:
            py.hotkey("down")       

            py.hotkey("down")
            py.hotkey("down")       

        py.hotkey("enter")
        n_tcs_rodados= 1
        while n_tcs_rodados<quantidade_tcs:
            self.ia.localiza("novo_tc.png", 0.7)
            self.ia.localiza("numero_serie.png", 0.7)
            py.doubleClick()        

            py.hotkey("del")
            if n_tcs_rodados ==1:
                py.write(tc_b)
            elif n_tcs_rodados ==2:
                py.write(tc_c)

            n_tcs_rodados=n_tcs_rodados+1

        return valor_tp


    def dados_medidor(self, rg, ult_calib, valor_tp, marca, modelo, versao):
        self.ia.localiza("medidores.png", 0.85)
        print(rg)
        py.write(str(rg))
        self.ia.localiza("numero_rg.png", 0.65)
        py.write(rg)
        self.ia.localiza("alg_comp.png", 0.65)
        print(ult_calib)
        # Ajustar a data com 1 dia a menos
       
        if valor_tp:
            py.hotkey("down")
        else:
            py.hotkey("down")
            py.hotkey("down")
        print(marca, modelo, versao)
        try:
            # Converte a string para um objeto datetime
            data_original = datetime.strptime(ult_calib, "%Y-%m-%d %H:%M:%S")
            # Subtrai 1 dia     

            data_ajustada = data_original - timedelta(days=1)
            # Converte de volta para string no formato desejado
            ult_calib_ajustada = data_ajustada.strftime("%d/%m/%Y")
            print(f"Data ajustada: {ult_calib_ajustada}")
        except ValueError:
            print("Erro: A data fornecida está em um formato inválido.")
            return


        
            
        py.hotkey("enter")
        self.tabzon(1)
        py.write(ult_calib_ajustada)
        self.tabzon(7)
        self.ia.localiza("fabricante_med.png", 0.6)
        if marca == "LANDIS+GYR":
            py.write("l")
            py.hotkey("enter")
        else:
            self.ia.localizar_palavra_rolando(marca, max_tentativas=20, scroll_pixels=1)

        self.ia.localiza("modelo_med.png", 0.6)
        self.ia.localizar_palavra_rolando(modelo, max_tentativas=20, scroll_pixels=1)
        self.ia.localiza("versao_firm.png", 0.6)
        self.ia.localizar_palavra_rolando(versao, max_tentativas=20, scroll_pixels=1)
        self.tabzon(2)

    def modelo_med(self, porta): 
        corrente_nom = '2,5'
        tensao_nom = '120'
        id_med = '1'
        ip = "27.0.140"
        
        porta= str(porta)
        print(porta)
        py.write(corrente_nom)
        self.tabzon(1)
        py.write(tensao_nom)
        self.tabzon(1)
        py.write(id_med)
        self.tabzon(1)
        py.write(ip)
        self.tabzon(1)
        py.write(porta)
        py.scroll(-1000)

        self.ia.localiza("atualizar.png", 0.8)
        comentario = 'Cadastro de ponto de medição cliente livre'
        py.write(comentario)

    def tabzon(self, numerodetabs):
        for tabs in range(numerodetabs):
            sleep(0.3)
            py.hotkey('tab')

    def pausar_execucao(self):
        """Pausa a execução aguardando a sinalização para continuar."""
        
        # Certifique-se de que o arquivo exista antes de entrar no loop
        if not os.path.exists(self.PAUSE_FILE):
            print(self.PAUSE_FILE)
            with open(self.PAUSE_FILE, 'w') as file:
                file.write('pausar')  # Escreva o estado inicial no arquivo
            print(f"Arquivo {self.PAUSE_FILE} criado para sinalizar pausa.")

        print("Execução pausada. Aguardando despausar...")
        
        while True:
            if os.path.exists(self.PAUSE_FILE):
                while True:  # Loop para verificar continuamente o conteúdo do arquivo
                    with open(self.PAUSE_FILE, 'r') as file:
                        status = file.read().strip()
                    if status == "despausar":
                        # Garanta que o arquivo está fechado antes de removê-lo
                        try:
                            os.remove(self.PAUSE_FILE)
                            print("Arquivo pause.txt removido com sucesso.")
                            print("Retomando...")
                            return  # Sai da função após retomar a execução
                        except PermissionError as e:
                            print(f"Erro ao remover o arquivo: {e}")
                            sleep(1)  # Espera antes de tentar novamente
                    else:
                        sleep(1)  # Previne que o loop consuma muita CPU
            else:
                print("Arquivo pause.txt não encontrado. Criando novamente...")
                with open(self.PAUSE_FILE, 'w') as file:
                    file.write('pausar')
                sleep(1)  # Espera antes de verificar novamente
        
    

class inf_planilha:
    """Tudo relacionado à planilha vai ficar aqui"""
    def __init__(self, caminho_planilha):
        self.caminho_planilha = caminho_planilha
        self.dados = None
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados da planilha em um DataFrame do Pandas e padroniza os nomes das colunas"""
        if os.path.exists(self.caminho_planilha):
            self.dados = pd.read_excel(self.caminho_planilha)
            
            # Padronizar nomes das colunas
            self._padronizar_nomes_colunas()

            # Tratar a coluna "UC"
            if 'UC' in self.dados.columns:
                self.dados['UC'] = self.dados['UC'].astype(str).str.strip()
                self.dados['UC'] = self.dados['UC'].str.replace(r'\.0$', '', regex=True)
        else:
            raise FileNotFoundError(f"Planilha não encontrada: {self.caminho_planilha}")

    def _padronizar_nomes_colunas(self):
        """Remove acentos, espaços e caracteres especiais dos nomes das colunas"""
        def remover_acentos(coluna):
            # Remove acentos
            coluna = ''.join(
                c for c in unicodedata.normalize('NFD', coluna)
                if unicodedata.category(c) != 'Mn'
            )
            # Remove caracteres especiais e substitui espaços por underscore
            coluna = re.sub(r'[^a-zA-Z0-9]', '_', coluna)
            # Remove underscores extras e espaços no final
            return coluna.strip('_')

        # Aplica a função de normalização a cada coluna
        self.dados.columns = [remover_acentos(col).strip() for col in self.dados.columns]

    def buscar_info_uc(self, uc):
        """Busca as informações de uma UC específica na planilha e armazena em variáveis específicas"""
        if self.dados is not None:
            # Converte a coluna "UC" e o valor de busca para string, removendo espaços em branco
            self.dados['UC'] = self.dados['UC'].astype(str).str.strip()
            self.dados['UC'] = self.dados['UC'].str.normalize('NFKD')  # Remove acentos ou caracteres especiais

            uc = str(uc).strip()
            print(self.dados['UC'].head())
            # Localiza a linha correspondente à UC
            info_uc = self.dados[self.dados['UC'] == uc]
            print("Linha selecionada:")
            print(info_uc)

            if not info_uc.empty:
                # Armazena as informações em variáveis específicas
                linha = info_uc.iloc[0]
            
                print("Valores brutos das colunas:")
                print(f"Marca: {linha['Marca']}, Modelo: {linha['Modelo']}, Versão: {linha['Firmware']}")


                def tratar_valor(valor):
                   
                    if pd.isna(valor):  
                        return None
                    return str(valor).strip()

                cod_ponto = tratar_valor(linha['Codigo_SCDE'])
                cliente = tratar_valor(linha['Cliente'])
                rg = tratar_valor(linha['RG'])
                municipio = tratar_valor(linha['Municipio'])
                regional = tratar_valor(linha['Regional'])
                etapa = tratar_valor(linha['Etapa'])
                ini_vig = tratar_valor(linha['Previsao_migracao'])
                cap_ger = tratar_valor(linha['Cap_GER'])
                cap_con = tratar_valor(linha['Cap_Consumo'])
                tc_a = tratar_valor(linha['TC_A'])
                tc_b = tratar_valor(linha['TC_B'])
                tc_c = tratar_valor(linha['TC_C'])
                ult_calib = tratar_valor(linha['Conclusao_MS_680'])
                porta = tratar_valor(linha['Porta'])
                rel_exis = tratar_valor(linha['RTC'])       
                tp_a = tratar_valor(linha['TP_A'])
                marca = tratar_valor(linha['Marca'])
                modelo = tratar_valor(linha['Modelo'])
                firmware = tratar_valor(linha['Firmware'])      


                # Retorna todas as variáveis
                return (cod_ponto, cliente, rg, municipio, regional, etapa, ini_vig, cap_ger, cap_con, tc_a, tc_b, tc_c, ult_calib, porta, rel_exis,tp_a, marca, modelo, firmware)
            else:
                print(f"UC {uc} não encontrada na planilha.")
        return None
    
# def main(lista_ucs, continuar_evento, usuario, senha):
def main(lista_ucs):
    print(lista_ucs)
    
    # Verifica se estamos em um ambiente PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    planilha = inf_planilha("assets\\excel\\plan_teste.xlsx")
    # ccee = page_ccee("https://operacao.ccee.org.br/")
    start = inserir_inf()
    # ccee.entrar_ccee(continuar_evento, usuario, senha)
    print(start.PAUSE_FILE)
    logging.basicConfig(filename=start.caminho_log, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
    logging.info(f"Iniciando lista de ucs: {lista_ucs}")
    for uc in lista_ucs:
        info = planilha.buscar_info_uc(uc) 
        if info:
            (cod_ponto, cliente, rg, municipio, regional, etapa, ini_vig, cap_ger, cap_con, tc_a, tc_b, tc_c, ult_calib, porta, rel_exis, tp_a, marca, modelo, firmware) = info
            marca = str(marca)

            while True:  # Loop para recomeçar a UC atual em caso de falha
                try:
                    print(f'Começando UC: {uc}')
                    # Substituir por suas operações antes da verificação da imagem
                    # start.ia.localiza("limpar.png", 0.6)
                    # start.ia.localiza("acoes.png", 0.7)
                    # start.ia.localiza("novo_ponto.png", 0.7)
                    # sleep(2)
                    # start.ia.localiza("ponto_mapeado.png", 0.8)
                    # py.write(cod_ponto)

                    # Verificação para encontrar a imagem da tela
                    if not start.ia.verifica("inicio_cadastro.png", 0.7):
                        print(f"Tela 'inicio_cadastro.png' não encontrada. Recomeçando UC: {uc}")
                        start.pausar_execucao()
                        continue  # Reinicia o loop para a mesma UC
                    
                    print(f"Informações para UC {uc}:")
                    print(f"Cliente: {cliente} \nCódigo SCDE: {cod_ponto} \nMunicípio: {municipio}")
                    print(f"Data vigência: {ini_vig}, {municipio}")
                    
                    #######################################################
                    start.start_cadastro()
                    start.inserir_dados_pnt_med(ini_vig, cap_ger, cap_con)
                    tcs = start.ver_tcs(tc_a, tc_b, tc_c)
                    start.localizacao(municipio)
                    #######################################################
                    valor_tp = start.trans_corren(tcs, tc_a, tc_b, tc_c, rel_exis, tp_a)
                    #######################################################
                    start.dados_medidor(rg, ult_calib, valor_tp, marca, modelo, firmware)
                    start.modelo_med(porta)
                    #######################################################
                    # Se tudo deu certo, sai do loop para a próxima UC
                    break

                except Exception as e:
                    logging.error(f"Erro ao processar UC: {uc}. Detalhes: {e}")
                    print(f"Erro ao processar UC: {uc}. Detalhes: {e}")
                    break  # Sai do loop em caso de erro crítico

if __name__ == "__main__":
    main(lista_ucs=[""])
    