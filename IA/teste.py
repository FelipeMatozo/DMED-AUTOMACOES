from datetime import datetime
import pyautogui as py

agora = datetime.now()
print(f"Data e hora: {agora}")
# Formatar a data e hora no formato desejado
formato = agora.strftime("%d%m%Y%H%M")
print(formato)
