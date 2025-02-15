from flask import Flask, render_template, request, jsonify,send_from_directory, url_for, redirect, make_response
import sys
import os
import pandas as pd
import re
import logging
import plotly.express as px
from IA import macro
from IA.CCEE import cadastro
from IA import concluir_T11
from IA import concluir_T12
from IA.portas_telemetrias import find_tm
from IA.gerador_ucs_antenas import buscar
from IA.banco_utils import exportar_para_excel
import plotly.graph_objs as go
import numpy as np
from time import sleep, time
import threading
import keyboard

app = Flask(__name__, static_folder='assets', template_folder='templates')
# Determine se estamos em um ambiente PyInstaller
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# Adicionar o caminho do diretório do projeto ao sys.path
project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_dir)

apps_dir = os.path.join(project_dir, 'apps')
sys.path.append(apps_dir)

# Adicionar o caminho do diretório 'IA' ao sys.path
macro_dir = os.path.join(project_dir, 'IA')
sys.path.append(macro_dir)

diretorio_base = os.path.dirname(os.path.abspath(__file__))
# Arquivo de controle de pausa/despaerweewrwe
PAUSE_FILE = os.path.join(diretorio_base, 'assets', 'txt', 'pause.txt')

@app.route('/despausar', methods=['POST'])
def despausar():
    """Despausa a execução alterando o arquivo pause.txt."""
    try:
        with open(PAUSE_FILE, 'w') as file:
            file.write('despausar')
        logging.info("Execução retomada pelo usuário.")
        return jsonify({'status': 'success', 'message': 'Execução retomada com sucesso!'}), 200
    except Exception as e:
        logging.error(f"Erro ao tentar despausar: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


CAMINHO_EXCEL = os.path.join(app.static_folder, 'excel')


# # Variável global de controle
# paused = threading.Event()


# # Função para monitorar a tecla 'Esc'
# def monitorar_teclado():
#     """
#     Monitora o teclado globalmente para detectar quando 'Esc' é pressionado.
#     Alterna entre pausar e retomar o programa, com controle de debouncing.
#     """
#     global paused
#     ultima_interacao = 0  # Armazena o timestamp da última interação

#     while True:
#         if keyboard.is_pressed("esc"):
#             agora = time()
#             if agora - ultima_interacao > 1:  # Tempo mínimo entre alternâncias (1 segundo)
#                 if paused.is_set():
#                     paused.clear()  # Retomar execução
#                     print("Execução retomada!")
#                 else:
#                     paused.set()  # Pausar execução
#                     print("Execução pausada!")
#                 ultima_interacao = agora
#             sleep(0.1)  # Pequena espera para evitar múltiplos eventos


# # Função de automação
# def automacao():
#     global paused
#     while True:
#         if paused.is_set():
#             print("Automação pausada...")
#             while paused.is_set():
#                 sleep(0.5)  # Aguarda enquanto pausado
#             print("Automação retomada!")
        
#         # Lógica da automação (exemplo)
#         print("Automação em execução...")
#         sleep(1)



def read_log(log_file_path_1='_internal\\assets\\log\\log.log', log_file_path_2='assets\\log\\log.log'):
    # Verifica se o primeiro caminho existe
    if os.path.exists(log_file_path_1):
        log_file_path = log_file_path_1
    # Verifica se o segundo caminho existe
    elif os.path.exists(log_file_path_2):
        log_file_path = log_file_path_2
    else:
        raise FileNotFoundError("O arquivo de log não foi encontrado em nenhum dos caminhos.")

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

    # Agrupa por Timestamp e Service Type, mantendo as UCs em uma lista
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S')  # Converte para datetime
    grouped_df = df.groupby(['Timestamp', 'Service Type', 'Macro']).agg({'UC': list}).reset_index()  # Mantém as UCs em uma lista
    grouped_df.rename(columns={'UC': 'UCs'}, inplace=True)  # Renomeia a coluna para 'UCs'

    return grouped_df, True


# Variável global para controlar a execução da thread
thread_running = False

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        ucs = request.form['ucs']
        # Dividir ucs por quebras de linha e remover espaços em branco
        ucs = ucs.splitlines()
        ucs = [uc.replace('\r', '').replace('\n', '').strip() for uc in ucs if uc.replace('\r', '').replace('\n', '').strip()]
        # Remover o último '1' se estiver presente
        if ucs and ucs[-1] == '1':
            ucs.pop()
        subtipo = request.form['subtipo']
        motivo = request.form['motivo']
        resp = request.form['resp']
        obs = request.form['obs']

        # Chamar a função main de macro.py e aguardar a conclusão
        macro.main(ucs, subtipo, motivo, resp, obs)

        # Exibir mensagem de sucesso após a conclusão
        return render_template('interface.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!")

    return render_template('interface.html')

# Variável para controlar a pausa
continuar_evento = threading.Event()

@app.route('/cadastro_ccee', methods=['GET', 'POST'])
def cadastro_page():
    global continuar_evento


    if request.method == 'POST':
        ucs = request.form['cadastro_ccee']
        
        # Processa a lista de UC's
        ucs = ucs.splitlines()
        ucs = [uc.strip() for uc in ucs if uc.strip()]
        print(ucs)
        # Define o evento de pausa
        continuar_evento.clear()
        threading.Thread(target=cadastro.main, args=(ucs,)).start()

        # Cria uma resposta para configurar o cookie
        response = make_response(redirect(url_for('cadastro_page')))
    

    # Renderiza a página e preenche o nome de usuário se o cookie estiver presente
    return render_template('cadastro_ccee.html')



# @app.route('/cadastro_ccee', methods=['GET', 'POST'])
# def cadastro_page():
#     if request.method == 'POST':
#         ucs = request.form['cadastro_ccee']
#         # Dividir ucs por quebras de linha e remover espaços em branco
#         ucs = ucs.splitlines()
#         ucs = [uc.replace('\r', '').replace('\n', '').strip() for uc in ucs if uc.replace('\r', '').replace('\n', '').strip()]

        
#         cadastro.main(ucs)
    
#         # Exibir mensagem de sucesso
#         return render_template('cadastro_ccee.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!")
#     return render_template('cadastro_ccee.html')


@app.route('/concluir_t11', methods=['GET', 'POST'])
def concluir_t11():
    if request.method == 'POST':
        ucs = request.form['concluir_t11']
        # Dividir ucs por quebras de linha e remover espaços em branco
        ucs = ucs.splitlines()
        ucs = [uc.replace('\r', '').replace('\n', '').strip() for uc in ucs if uc.replace('\r', '').replace('\n', '').strip()]
        motivo = request.form['motivo']
        obs = request.form['obs']

        # Passar os dados para a função concluir_T11
        concluir_T11.main(ucs, motivo, obs)

        # Exibir mensagem de sucesso
        return render_template('concluir_t11.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!")

    return render_template('concluir_t11.html')

@app.route('/download')
def download_log():
    return send_from_directory(directory='assets/log', path='log.log', as_attachment=True)

@app.route('/gerar_t11', methods=['GET', 'POST'])
def gerar_t11():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('gerar_t11.html')


@app.route('/concluir_t10', methods=['GET', 'POST'])
def concluir_t10():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('concluir_t10.html')

@app.route('/concluir_t12', methods=['GET', 'POST'])
def concluir_t12():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('concluir_t12.html')

@app.route('/concluir_ss_t12', methods=['GET', 'POST'])
def concluir_ss_t12():
    if request.method == 'POST':
        ucs = request.form['concluir_t12']
        # Dividir ucs por quebras de linha e remover espaços em branco
        ucs = ucs.splitlines()
        ucs = [uc.replace('\r', '').replace('\n', '').strip() for uc in ucs if uc.replace('\r', '').replace('\n', '').strip()]
        motivo = request.form['motivo']
        obs = request.form['obs']
 
        # Passar os dados para a função concluir_T11
        concluir_T12.main(ucs, motivo, obs)

        # Exibir mensagem de sucesso
        return render_template('concluir_ss_t12.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!")
    return render_template('concluir_ss_t12.html')

@app.route('/gerar_t12', methods=['GET', 'POST'])
def gerar_t12():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('gerar_t12.html')

@app.route('/conclusao', methods=['GET', 'POST'])
def conclusao():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('conclusao.html')

@app.route('/geracao', methods=['GET', 'POST'])
def geracao():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('geracao.html')

@app.route('/menu_rpas_T12', methods=['GET', 'POST'])
def menu_rpas_T12():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('menu_rpas_T12.html')


# Função para criar a pasta, caso não exista
def criar_pasta_excel():
    if not os.path.exists(CAMINHO_EXCEL):
        os.makedirs(CAMINHO_EXCEL)

@app.route('/portas_telemetrias', methods=['GET', 'POST'])
def portas_telemetrias():
    if request.method == 'POST':
        telemetrias = request.form.get('telemetrias', '').strip()
        if not telemetrias:
            return render_template('portas_telemetrias.html', mensagem_erro="Campo 'telemetrias' não pode estar vazio.")
        

        telemetrias_lista = find_tm(telemetrias)

        
        # Exibir mensagem de sucesso
        return render_template('portas_telemetrias.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!", telemetrias_valor="\n".join(telemetrias_lista))
    
    return render_template('portas_telemetrias.html')

@app.route('/download_excel', methods=['GET', 'POST'])
def download_excel():
    if request.method == 'POST':
        telemetrias = request.form.get('telemetrias', '').strip()
        if not telemetrias:
            return render_template('portas_telemetrias.html', mensagem_erro="Campo 'telemetrias' não pode estar vazio.")
        
        # Dividir a string de telemetrias em uma lista, se necessário
        # Dividir a string de telemetrias em uma lista
        valores = telemetrias.splitlines()  # Dividir por quebras de linha # Supondo que os valores sejam separados por vírgulas
        # Adicionar "00" à esquerda de cada valor
        print(valores)
        # Criar o diretório, caso não exista
        criar_pasta_excel()
        valores_tratados = [f'00{valor.strip()}' for valor in valores]
        # Gerar o arquivo Excel usando a função exportar_para_excel
        caminho_arquivo_excel = os.path.join(CAMINHO_EXCEL, 'dados_tms.xlsx')
        exportar_para_excel('IRIS', 'codigo_tm', valores=valores_tratados, caminho_arquivo_excel=caminho_arquivo_excel)

        # return render_template('portas_telemetrias.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!", telemetrias_valor=telemetrias)

    return send_from_directory(directory=CAMINHO_EXCEL, path='dados_tms.xlsx', as_attachment=True)

@app.route('/mapa', methods=['GET', 'POST'])
def mapa():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('mapa.html')

@app.route('/mapa_uc', methods=['POST'])
def mapa_uc():
    if request.method == 'POST':
        uc = request.form['uc']
        
        # Gera o nome do arquivo do mapa baseado na UC fornecida
        mapa_filename = f'mapa_{uc}.html'
        mapa_filepath = os.path.join('SISTEMA_RPA_DMED', 'assets', 'html', mapa_filename)
        
        # Chama a função que gera o mapa
        buscar(uc)  # Supondo que buscar salva o mapa com o nome correto
        
        # Renderiza o template e passa o nome do arquivo do mapa gerado
        return render_template('mapa.html', mapa_gerado=mapa_filename)
    
    return render_template('mapa.html')


@app.route('/exibir_mapa')
def exibir_mapa():
    # Renderiza o template com o mapa incluído
    return render_template('mapa.html')


@app.route('/gerar_t10', methods=['GET', 'POST'])
def gerar_t10():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('gerar_t10.html')

@app.route('/localiza_antenas', methods=['GET', 'POST'])
def localiza_antenas():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('localiza_antenas.html')

@app.route('/versions', methods=['GET'])
def versions():
    if request.method == 'POST':
        # Processar o POST se necessário
        pass
    return render_template('versions.html')

@app.route('/dashboards')
def dashboards():
    return render_template('dashboard.html')

@app.route('/dashboards/table_data', methods=['GET'])
def table_data():
    df, success = read_log()
    if not success or df.empty:
        return {"error": "Não há dados disponíveis."}, 404
    
    # Converte o DataFrame para dicionário
    table_data = df.to_dict(orient='records')
    return jsonify(table_data)

@app.route('/dashboards/uc_data')
def uc_data():
    df, success = read_log()
    if success:
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify([])

@app.route('/dashboards/data')
def dashboard_data():
    df, _ = read_log()
    if df.empty:
        return {"error": "Não há dados disponíveis."}, 404

    # Criar um gráfico baseado nos dados
    fig = px.bar(df, x="Timestamp", y="UCs", color="Service Type", title="Histograma de UCs por Serviço e Dia")
    fig.update_layout(height=300)

    graphJSON = fig.to_json()
    return jsonify(graphJSON)

if __name__ == '__main__':
    #  # Inicia o thread para monitorar o teclado
    # teclado_thread = threading.Thread(target=monitorar_teclado, daemon=True)
    # teclado_thread.start()
     
    # # Inicia o thread para executar a automação
    # automacao_thread = threading.Thread(target=automacao, daemon=True)
    # automacao_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
