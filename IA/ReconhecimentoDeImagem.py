import pyautogui as py
import os
import time
from time import sleep
class Reconhecimento:
    
    def __init__(self, numeroDeTentativasMax=5, delay=0.7):
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
                
    def inf(self, image_path, precisao ):

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
                if self.tentativasRealizadas >= 3:
                    self.tentativasRealizadas = 0
                    return False
    
    def popup(self):

        self.tentativasRealizadas = 0
        diretorioDaImagen = os.path.join(self.raizDoProjeto, 'assets', 'images', 'pop_up.PNG')  
        lida_check= os.path.join(self.raizDoProjeto, 'assets', 'images', 'lida_check.png') 
        while self.online:

            time.sleep(self.delay+0.5)
            
            try:
                tela_encontrada = py.locateOnScreen(diretorioDaImagen, confidence=0.6)
                if tela_encontrada is not None:
                    py.moveTo(tela_encontrada)
                    print('há pop up')
                    self.localiza(lida_check,0.7)
                    self.localiza('check_box.png',0.7)
                    py.click(py.moveRel(0,+59))
                    py.moveTo(tela_encontrada)
                    sleep(1)
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
                if self.tentativasRealizadas >= 7:
                    self.online = False
                    break
                