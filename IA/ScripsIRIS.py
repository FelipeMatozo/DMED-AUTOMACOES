import subprocess
from time import sleep
from ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import pyperclip
import os
import sys
import sqlite3

class consultaIris():
    
    def __init__(self):

        self.ia = Reconhecimento(numeroDeTentativasMax=15, delay=0.2)


    def consultarUC(self,numeroDaUC):
        programa = programasExecutaveis()
        programa.abrir()

        print(numeroDaUC)
        self.ia.cliqueDuplo('Conectar.png',0.8)
        self.ia.localiza('bt_listagem_telemetria.PNG', 0.7)
        self.ia.localiza('Config.PNG', 0.7)
        self.ia.localiza('Config_Bot_cobertura.PNG', 0.6)
        py.hotkey('down')
        py.hotkey('down')
        self.ia.localiza('bt_confirmar.PNG', 0.7)
        py.hotkey('enter')
        self.ia.localiza('tl_listagem_telemetrias.png', 0.65)
        py.click(py.moveRel(372,-174))
        self.ia.localiza('barra.png', 0.6)
        py.click(py.moveRel(30,15))
        py.write(numeroDaUC)
        py.hotkey('enter')
        self.ia.inf('nome.png', 0.65)
        py.click(py.moveRel(-100,10))
        
        py.drag(780, 0, duration=1)

        py.hotkey('ctrl', 'c')

        programa.fechar()

        valorEncontrado = pyperclip.paste()
        
        return valorEncontrado
 
class programasExecutaveis():

    def __init__(self):
        self.caminho_iris = r"C:\Program Files (x86)\CAS\Iris Manager\iris-manager.exe"
        self.processo = None  # Armazena a referência ao processo
        self.pid = ""
        
    def abrir(self):
        self.processo = subprocess.Popen(self.caminho_iris)
        self.pid = self.processo.pid
        print(f"Iris Manager iniciado com PID {self.processo.pid}")


    def fechar(self):
        # Fecha o processo verificando cada processo ativo e comparando o caminho executável
        py.click(1900,5)
        sleep(0.2)
        py.click(1900,5)

    # Exemplo de uso

class banco:
    def __init__(self):
    
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.banco = os.path.join(self.script_dir, '..', 'banco', 'banco_dmed')

    def add_banco(self, UC, ID, CODIGO_DO_PONTO, PORTA_TM):

        con = sqlite3.connect(self.banco)
        cursor = con.cursor()

        # Verifica se a combinação de UC e ID já existe na tabela
        cursor.execute("SELECT UC, ID FROM IRIS WHERE UC = ? AND ID = ?", (UC, ID))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"A combinação UC {UC} e ID {ID} já existe na tabela.")
        else:
            # Insere novos dados na tabela
            cursor.execute("INSERT INTO IRIS (UC, ID, CODIGO_DO_PONTO, PORTA_TM) VALUES (?, ?, ?, ?)",
                        (UC, ID, CODIGO_DO_PONTO, PORTA_TM))
            con.commit()
            print(f"Dados inseridos com sucesso: UC {UC}, ID {ID}, CODIGO DO PONTO {CODIGO_DO_PONTO}, PORTA TM {PORTA_TM}.")
        
        con.close()


   

def main(mensagem):
    programa = consultaIris()
    string = programa.consultarUC(mensagem)
    return string

if __name__ == '__main__':
    main('0044701204')  
