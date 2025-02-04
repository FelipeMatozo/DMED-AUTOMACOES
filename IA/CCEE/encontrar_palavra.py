from time import sleep
import pyautogui
from pytesseract import pytesseract, Output
from PIL import Image
import time
import os
from unidecode import unidecode  # Import necessário para remover acentos

diretorio_base = os.path.dirname(os.path.abspath(__file__),)
os.environ['TESSDATA_PREFIX'] = os.path.join(os.path.dirname(os.path.dirname(diretorio_base)), 'Tesseract-OCR')
        

# # Defina o caminho para a pasta onde o Tesseract foi instalado
# os.environ['TESSDATA_PREFIX'] = r"C:\Users\L805958\dmed\SISTEMA_RPA_DMED\Tesseract-OCR"

# # Defina o caminho para o executável do Tesseract
# pytesseract.tesseract_cmd = r"C:\Users\L805958\dmed\SISTEMA_RPA_DMED\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = os.path.join(os.path.dirname(os.path.dirname(diretorio_base)), 'Tesseract-OCR','tesseract.exe')
        

def localizar_palavra_rolando(palavras, max_tentativas=10, scroll_pixels=-300, lang="por"):
    """Procura palavras na tela rolando até encontrá-las e clica nelas."""
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

        # Procura pelas palavras
        for palavra in palavras:
            palavra_limpa = unidecode(palavra.lower())  # Remove acentos e transforma para minúsculas
            for i, texto in enumerate(resultados['text']):
                if unidecode(texto.lower()) == palavra_limpa:  # Remove acentos e compara em minúsculas
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

    print(f'Nenhuma palavra encontrada após {max_tentativas} tentativas.')

sleep(3)
