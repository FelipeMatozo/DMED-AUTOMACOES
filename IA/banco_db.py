import os
import sys
import sqlite3

class banco:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.banco = os.path.join(self.script_dir, '..', 'banco', 'banco_dmed')

    def banco(self):

        con = sqlite3.connect(self.script_dir)
        cursor = con.cursor()

        # Verifica se o SERIAL já existe na tabela
        cursor.execute("SELECT SERIAL FROM serial_uc WHERE SERIAL = ?", (,))
        existing_serial = cursor.fetchone()

        if existing_serial:
            print(f"O  {} já existe na tabela.")
        else:
            # Inserir os valores de SERIAL e UC_1 na tabela serial_uc
            cursor.execute("INSERT INTO serial_uc () VALUES (?, ?)", (, ))
            con.commit()
            print(f"UC {} inserido com sucesso.")
        
        con.close()

    