import csv
import subprocess
from time import sleep
from ReconhecimentoDeImagem import Reconhecimento
import pyautogui as py
import sys
import os
import logging

ia = Reconhecimento(numeroDeTentativasMax=7, delay=1.5)

while ia.localiza_1x('telainicial.png', 0.6)== False:
    ia.localiza_1x('portinha.png', 0.7)