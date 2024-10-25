from flask import Flask, render_template, request, jsonify,send_from_directory, url_for, redirect
import sys
import os
import pandas as pd
import re
import logging
import plotly.express as px

import plotly.graph_objs as go
import numpy as np
from time import sleep
import threading

def read_log(log_file_path='assets\\log\\log.log'):
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"O arquivo de log não foi encontrado: {log_file_path}")

    data_list = []

    # Ler o arquivo de log
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()

    # Processar cada linha do log
    for line in log_lines:
        # Usando uma expressão regular que aceita "UC:" ou "SS:"
        match = re.search(r'(\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}) - (UC|SS): (\d+) finalizada! Servico: T(\d+) Macro: (\w+)', line)
        if match:
            timestamp = match.group(1)  # Data e hora
            uc_number = match.group(3)   # Número da UC ou SS
            service_type = 'T' + match.group(4)  # Tipo de serviço
            macro_tipo = match.group(5)  # Tipo da macro
            # Adiciona uma entrada ao data_list
            data_list.append({
                'Timestamp': timestamp,
                'UC': uc_number,
                'Service Type': service_type,
                'Macro': macro_tipo
            })

    # Cria um DataFrame a partir da lista
    df = pd.DataFrame(data_list)
    if df.empty:
        print("Nenhum dado encontrado no log.")
        return df, False  # Retorna DataFrame vazio e indicador de dados não encontrados
    print(df)
    # Agrupa por Timestamp e Service Type, mantendo as UCs em uma lista
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S')  # Converte para datetime
    grouped_df = df.groupby(['Timestamp', 'Service Type']).agg({'UC': list}).reset_index()  # Mantém as UCs em uma lista
    grouped_df.rename(columns={'UC': 'UCs'}, inplace=True)  # Renomeia a coluna para 'UCs'

    print(df)
    return grouped_df, True

if __name__ == '__main__':
    read_log()