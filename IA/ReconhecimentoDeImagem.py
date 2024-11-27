import pyautogui as py
import os, sys
import time
from time import sleep
import pytesseract
from pytesseract import pytesseract,Output
import pyautogui
from PIL import Image

from unidecode import unidecode  # Importando a biblioteca unidecode

# Defina o caminho para a pasta onde o Tesseract foi instalado
os.environ['TESSDATA_PREFIX'] = r"C:\Users\L805958\dmed\SISTEMA_RPA_DMED\Tesseract-OCR"

# Defina o caminho para o executável do Tesseract
pytesseract.tesseract_cmd = r"C:\Users\L805958\dmed\SISTEMA_RPA_DMED\Tesseract-OCR\tesseract.exe"



class Reconhecimento:
    
    def __init__(self, numeroDeTentativasMax, delay):
        """
        A ideia dessa def do codigo é onde as variaveis das outras 
        defs sao definidas, sao variaveis de uso da classe.
        """
        self.numeroDeTentativasMax = numeroDeTentativasMax
        self.delay = float(delay)
        self.tentativasRealizadas = 0
        self.online = True
        self.diretorioLocal = os.path.dirname(__file__)
        self.raizDoProjeto = os.path.join(self.diretorioLocal, '..')

    def localiza(self, image_path, precisao):
        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', image_path)
        

        while self.online:

            time.sleep(self.delay)

            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=precisao)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    py.click()
                    print(f"A tela {nome_imagem} foi encontrada.")
                    return True
                    
                else:
                    print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                    time.sleep(1) 
                    self.tentativasRealizadas += 1
                    if self.tentativasRealizadas >= self.numeroDeTentativasMax:
                        self.online = False
                        return False
            except:
                print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                self.tentativasRealizadas += 1
                if self.tentativasRealizadas >= self.numeroDeTentativasMax:
                    self.online = False
                    return False

    def localiza_1x(self, image_path, precisao):
        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', image_path)
        

        while self.online:

            time.sleep(self.delay)

            try:
                print("tentando localizar tela")
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=precisao)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    py.click()
                    print(f"A tela {nome_imagem} foi encontrada.")
                    return True
                    
                else:
                    print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                    time.sleep(1) 
                
                    return False
            except:
                print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                return False

    def cliqueDuplo(self, image_path, precisao):

        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """

        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', image_path)

        self.tentativasRealizadas = 0

        while self.online:
        
            time.sleep(self.delay)

            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=precisao)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    py.doubleClick()
                    print(f"A tela {nome_imagem} foi encontrada.")
                    break  
            except:
                print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                self.tentativasRealizadas += 1
                if self.tentativasRealizadas >= self.numeroDeTentativasMax:
                    self.tentativasRealizadas = 0
                    self.online = False
                    break
                
    def inf(self, image_path, precisao):

        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', image_path)

    
        while self.online:

            time.sleep(self.delay)

            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=precisao)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    print(f"A tela {nome_imagem} foi encontrada.")
                    return True 
            except:
                print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                self.tentativasRealizadas += 1
                if self.tentativasRealizadas >= 4:
                    self.tentativasRealizadas = 0
                    return False
    
    def popup(self):

        self.tentativasRealizadas = 0
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', 'pop_up.PNG')  
        lida_check= os.path.join(self.raizDoProjeto, 'assets', 'images', 'lida_check.png') 
        while self.online:

            time.sleep(self.delay)
            
            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=0.55)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    print('há pop up')
                    self.localiza(lida_check,0.7)
                    self.localiza('check_box.png',0.7)
                    sleep(0.2)
                    py.click(py.moveRel(0,+59))
                    sleep(0.2)
                    py.moveTo(tela_encontrada)
                    sleep(0.2)
                    py.click(py.moveRel(+229,+178))
                    break
                else:
                    print(f"Tela PopUP não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                    time.sleep(1) 
                    self.tentativasRealizadas += 1
                    if self.tentativasRealizadas >= 5:
                        self.online = False
                        break
            except:
                print(f"Tela PopUP não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                self.tentativasRealizadas += 1
                if self.tentativasRealizadas >= 5:
                    self.tentativasRealizadas = 0
                    self.online = False
                    break


    def verifica(self, image_path, precisao):
        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', image_path)
    

        while self.online:

            time.sleep(1)

            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=precisao)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    print(f"A tela {nome_imagem} foi encontrada.")
                    return True  
                    
            except:
                print(f"Tela {nome_imagem} não foi encontrada,Tentativa {self.tentativasRealizadas + 1}")
                time.sleep(1) 
                self.tentativasRealizadas += 1
                if self.tentativasRealizadas >= self.numeroDeTentativasMax:
                    self.online = False
                    break
    
    def localizar_palavra_rolando(self, palavra, max_tentativas=10, scroll_pixels=-300, lang="por"):
        """Procura uma palavra na tela rolando até encontrá-la e clica nela."""
        # Remove os acentos da palavra passada como argumento
        palavra_sem_acento = unidecode(palavra.lower())
        
        tentativa = 0
        while tentativa < max_tentativas:
            # Captura a tela atual
            screenshot_path = 'tela.png'
            pyautogui.screenshot(screenshot_path)
            imagem = Image.open(screenshot_path)

            # Realiza OCR na imagem com o caminho explícito do tessdata
            resultados = pytesseract.image_to_data(
                imagem,
                lang=lang,
                config="--tessdata-dir C:/Users/L805958/dmed/SISTEMA_RPA_DMED/Tesseract-OCR/tessdata --psm 6 --oem 1",
                output_type=Output.DICT
            )

            # Procura pela palavra
            for i, texto in enumerate(resultados['text']):
                # Comparar o texto detectado sem modificar, mas a palavra passada será sem acento
                if unidecode(texto.lower()) == palavra_sem_acento:  # Ignora acentos da palavra passada
                    x, y, w, h = (resultados['left'][i], resultados['top'][i],
                                resultados['width'][i], resultados['height'][i])
                    centro_x = x + w // 2
                    centro_y = y + h // 2

                    # Move e clica na posição encontrada
                    pyautogui.click(centro_x, centro_y)
                    print(f'Palavra "{palavra}" encontrada e clicada!')
                    return True

            # Se não encontrou, rola a tela e tenta novamente
            pyautogui.scroll(scroll_pixels)  # Scroll para cima (-) ou para baixo (+)
            tentativa += 1
            time.sleep(1)  # Pequena pausa para a rolagem ser processada

        print(f'Palavra "{palavra}" não encontrada após {max_tentativas} tentativas.')

                