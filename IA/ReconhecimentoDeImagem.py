import pyautogui as py
import os
import time
from time import sleep
import pytesseract
from pytesseract import Output
from PIL import Image, ImageOps
from unidecode import unidecode
from pathlib import Path
import subprocess
from PIL import ImageEnhance
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import unicodedata
from unidecode import unidecode

from pathlib import Path
# Caminho base do projeto
base_path = Path(__file__).resolve().parent.parent

# Caminho dinâmico do Tesseract e tessdata
tesseract_path = base_path / "Tesseract-OCR" / "tesseract.exe"
tessdata_path = base_path / "Tesseract-OCR" / "tessdata"

# Verifica se o executável do Tesseract existe antes de definir
if not tesseract_path.exists():
    raise FileNotFoundError(f"Erro: O Tesseract não foi encontrado no caminho esperado: {tesseract_path}")

# Configura as variáveis de ambiente dinamicamente
pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
os.environ['TESSDATA_PREFIX'] = str(tessdata_path)

print(f"Tesseract configurado corretamente: {tesseract_path}")
print(f"Tessdata directory: {tessdata_path}")

# # Verifica se o Tesseract existe e pode ser executado
# if not Path(pytesseract.pytesseract.tesseract_cmd).exists():
#     raise FileNotFoundError(f"Tesseract não encontrado no caminho: {pytesseract.pytesseract_cmd}")
# try:
#     resultado = subprocess.run([pytesseract.pytesseract.tesseract_cmd, "--version"], capture_output=True, text=True, check=True)
#     print(f"✅ Tesseract encontrado: {resultado.stdout}")
# except Exception as e:
#     raise RuntimeError(f"Erro ao executar o Tesseract: {e}")

class Reconhecimento:
    def __init__(self, numeroDeTentativasMax, delay):
        self.numeroDeTentativasMax = numeroDeTentativasMax
        self.delay = float(delay)
        self.tentativasRealizadas = 0
        self.online = True
        self.diretorioLocal = os.path.dirname(__file__)
        self.raizDoProjeto = os.path.join(self.diretorioLocal, '..')

    # def localizar_palavra_rolando(self, palavra, max_tentativas=10, scroll_pixels=-300, lang="por"):
    #     palavra_sem_acento = unidecode(palavra.lower())
    #     tentativa = 0
    #     while tentativa < max_tentativas:
    #         screenshot_path = 'tela.png'
    #         py.screenshot(screenshot_path)
    #         imagem = Image.open(screenshot_path)

    #         # Aplica zoom, filtro de nitidez e ajuste de contraste
    #         imagem_zoom = imagem.resize((imagem.width * 2, imagem.height * 2), Image.LANCZOS)
    #         imagem_zoom = imagem_zoom.filter(ImageFilter.SHARPEN)
    #         imagem_zoom = ImageEnhance.Contrast(imagem_zoom).enhance(3.0)
    #         imagem_zoom = ImageOps.invert(imagem_zoom.convert('L'))

    #         config = f"--tessdata-dir {os.environ['TESSDATA_PREFIX']} --psm 6 --oem 3 -c preserve_interword_spaces=1"
    #         texto_detectado = pytesseract.image_to_string(imagem_zoom, lang=lang, config=config)

    #         if palavra_sem_acento in unidecode(texto_detectado.lower()):
    #             print(f'Texto completo "{palavra}" detectado.')
    #             try:
    #                 x, y = py.locateCenterOnScreen(screenshot_path, confidence=0.8)
    #                 print(x, y)
    #                 py.click(x, y)
    #                 print(f'Texto completo "{palavra}" encontrado e clicado exatamente!')
    #                 return True
    #             except:
    #                 print("Não foi possível localizar a palavra visualmente na tela, mas o OCR detectou.")

    #         py.scroll(scroll_pixels)
    #         tentativa += 1
    #         time.sleep(1)
    #         print(f"Tentativa {tentativa}: Buscando '{palavra}'")

    #     print(f'Texto completo "{palavra}" não encontrado após {max_tentativas} tentativas.')

    
    def normalizar_texto(self, texto):
        """Remove espaços extras e converte para minúsculas sem modificar caracteres acentuados."""
        return texto.lower().strip()


    def localizar_palavra_rolando(self, palavra, max_tentativas=10, scroll_pixels=-300, lang="por"):
        """Procura uma palavra ou frase na tela rolando até encontrá-la e clica no centro do conjunto."""
        
        palavra_normalizada = self.normalizar_texto(palavra)
        palavras = palavra_normalizada.split()  # Divide a frase em palavras separadas

        tentativa = 0
        while tentativa < max_tentativas:
            # Captura a tela atual
            screenshot_path = 'tela.png'
            py.screenshot(screenshot_path)
            imagem = Image.open(screenshot_path)
            imagem = imagem.resize((imagem.width * 2, imagem.height * 2), Image.LANCZOS)
            imagem = imagem.filter(ImageFilter.SHARPEN)
            imagem = ImageEnhance.Contrast(imagem).enhance(5.0)
            # imagem = ImageOps.invert(imagem.convert('L'))

            resultados = pytesseract.image_to_data(
                imagem,
                lang=lang,
                config="--psm 6 --oem 3 -c preserve_interword_spaces=1",
                output_type=Output.DICT
            )



            num_palavras = len(palavras)
            for i in range(len(resultados['text']) - num_palavras + 1):
                # Normaliza as palavras detectadas pelo OCR para comparação
                palavras_ocr = [self.normalizar_texto(resultados['text'][i + j]) for j in range(num_palavras)]

                # Verifica se todas as palavras consecutivas aparecem na mesma linha
                if palavras_ocr == palavras and all(resultados['top'][i + j] == resultados['top'][i] for j in range(num_palavras)):  
                    # Calcula a média das posições das palavras encontradas
                    x1 = resultados['left'][i]
                    x2 = resultados['left'][i + num_palavras - 1] + resultados['width'][i + num_palavras - 1]
                    y1 = resultados['top'][i]
                    y2 = resultados['top'][i] + resultados['height'][i]

                    centro_x = ((x1 + x2) // 2) // 2  # Ajuste da escala
                    centro_y = ((y1 + y2) // 2) // 2  # Ajuste da escala

                    # Move e clica na posição corrigida
                    py.click(centro_x, centro_y)

                    print(f'Frase "{palavra}" encontrada e clicada!')
                    return True

            # Se não encontrou, rola a tela e tenta novamente
            py.scroll(scroll_pixels)
            tentativa += 1
            time.sleep(1)

        print(f'Frase "{palavra}" não encontrada após {max_tentativas} tentativas.')
        return False


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
    
    def localiza_ccee(self, image_path, precisao):
        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images_ccee', image_path)
        

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
        self.online = True

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

    def verifica_ccee(self, image_path, precisao):
        """
        Funçao localiza a imagem na tela, ela tenta localizar com um "numeroDeTentativasMax"
        se nao for possivel ela informa o usuario que a imagem nao esta na tela
        se for, ele move até a tela e clica na imagem
        """
        self.tentativasRealizadas = 0
        nome_imagem = os.path.basename(image_path)
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images_ccee', image_path)
        print(diretorioDaImagen)
        self.online = True

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
    
    

                