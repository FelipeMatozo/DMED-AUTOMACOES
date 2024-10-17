from flask import Flask, render_template, request, jsonify,send_from_directory, url_for, redirect
import sys
import os
import pandas as pd
import re
import logging
import plotly.express as px
from IA import macro
from IA import concluir_T11
from IA.portas_telemetrias import find_tm
from IA.gerador_ucs_antenas import buscar
from IA.banco_utils import exportar_para_excel
import plotly.graph_objs as go
import numpy as np

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

# Determine se estamos em um ambiente PyInstaller
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# Adicionar o caminho do diretório do projeto ao sys.path
project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_dir)

# Adicionar o caminho do diretório 'IA' ao sys.path
macro_dir = os.path.join(project_dir, 'IA')
sys.path.append(macro_dir)




CAMINHO_EXCEL = os.path.join(app.static_folder, 'excel')


def read_log():
    log_file_path = 'assets\\log\\log.log'  # Coloque o caminho absoluto se necessário
    logging.info(f"Tentando ler o arquivo de log em: {os.path.abspath(log_file_path)}")

    # Tente abrir o arquivo de log
    if not os.path.exists(log_file_path):
        logging.error("Arquivo de log não encontrado.")
        return pd.DataFrame(), False  # Retorna DataFrame vazio se o arquivo não existir

    data_list = []

    try:
        with open(log_file_path, 'r') as file:
            log_lines = file.readlines()
            print(log_lines)  # Para depuração, remova ou comente em produção
    except Exception as e:
        logging.error(f"Erro ao abrir o arquivo de log: {str(e)}")
        return pd.DataFrame(), False  # Retorna DataFrame vazio se houver um erro

    # Processa as linhas do log
    for line in log_lines:
        # Captura a data, UC e tipo de serviço com regex
        date_match = re.search(r'(\d{2}-\d{2}-\d{4}) \d{2}:\d{2}:\d{2} - UC: \d+ finalizada! (?:Serviço|Servico): (T\d+)', line)

        if date_match:
            current_date = date_match.group(1)  # Captura a data
            current_service = date_match.group(2)  # Captura o tipo de serviço
            
            # Adiciona uma entrada ao data_list
            data_list.append({
                'Data': current_date,
                'UCs': 1,  # Contabiliza cada UC
                'Tipo de serviço': current_service
            })

    # Cria um DataFrame a partir da lista
    df = pd.DataFrame(data_list)
    print(df)  # Para depuração, remova ou comente em produção
    if df.empty:
        logging.warning("Nenhum dado encontrado no log.")
        return df, False  # Retorna DataFrame vazio e indicador de dados não encontrados

    # Agrupa por Data e Tipo de serviço, somando as UCs
    df = df.groupby(['Data', 'Tipo de serviço']).agg({'UCs': 'sum'}).reset_index()
    print(df)  # Para depuração, remova ou comente em produção
    return df, True  # Retorna o DataFrame e indicador de dados encontrados

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

        # Passar os dados para a função main de macro.py
        macro.main(ucs, subtipo, motivo, resp, obs)

        # Exibir mensagem de sucesso
        return render_template('interface.html', mensagem_sucesso="Sua solicitação foi enviada com sucesso!")

    return render_template('interface.html')


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
    df, _ = read_log()  # Aqui, garantimos que estamos desempacotando corretamente
    
    # Verifique se a coluna 'Data' está presente no DataFrame
    if 'Data' not in df.columns:
        print("Coluna 'Data' não encontrada no DataFrame.")
        print(df.head())  
        return {"error": "Coluna 'Data' não encontrada no DataFrame."}, 500
    
    # Formatar a data
    df['Data'] = pd.to_datetime(df['Data'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')  
    
    # Converte o DataFrame para dicionário para enviar como resposta JSON
    table_data = df.to_dict(orient='records')
    
    return jsonify(table_data)

@app.route('/dashboards/uc_data')
def uc_data():
    df, success = read_log()  # Certifique-se de que o DataFrame correto está sendo retornado
    if success:
        return render_template('dashboard.html', table_data=df.to_dict(orient='records'))
    else:
        return render_template('dashboard.html', table_data=None)


@app.route('/dashboards/uc_data', methods=['GET'])
def dashboard_uc_data():
    try:
        # Suponha que 'fig' é o objeto que você deseja converter
        # Primeiro, converta fig para um dicionário e verifique seu conteúdo
        fig_dict = fig.to_dict()

        # Aqui você deve converter os arrays NumPy para listas, se houver
        for key, value in fig_dict.items():
            if isinstance(value, np.ndarray):  # Se o valor for um ndarray
                fig_dict[key] = value.tolist()  # Converta para lista

        return jsonify(fig_dict)

    except Exception as e:
        logging.error(f"Erro ao gerar dados do dashboard: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/dashboards/data')
def dashboard_data():
    df, _ = read_log()  # Certificando-se de que estamos desempacotando corretamente
    
    if df.empty:
        return {"error": "Não há dados disponíveis."}, 404
    
    fig = px.bar(df, x="Data", y="UCs", color="Tipo de serviço", title="Histograma de UCs por Serviço e Dia")
    
    # Aumentar o tamanho do gráfico
    fig.update_layout(height=300)
    
    graphJSON = fig.to_json()
    return jsonify(graphJSON)

@app.route('/dashboards/table_data')
def dashboard_table_data():
    df, _ = read_log()
    
    if df.empty:
        return {"error": "Não há dados disponíveis."}, 404
    
    table_data = df.to_dict(orient='records')
    return jsonify(table_data)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
