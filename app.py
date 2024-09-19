from flask import Flask, render_template, request, jsonify,send_from_directory, url_for, redirect
import sys
import os
import pandas as pd
import plotly.express as px
from IA import macro
from IA import concluir_T11
from IA.portas_telemetrias import find_tm
from IA.gerador_ucs_antenas import buscar
from IA.banco_utils import exportar_para_excel

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
    log_path = os.path.join(app.static_folder, 'log', 'log.log')
    with open(log_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    ucs_data = []
    current_config = None
    for line in lines:
        if "Configuracao" in line:
            parts = line.split(': ')
            current_config = parts[1].split(',')[0]  # Pega apenas a primeira parte antes da vírgula
        if "Rodando UC's" in line:
            datetime_str = ' '.join(line.split(' ')[:2])  # A data e hora estão no início da linha
            ucs_str = line.split(': ')[-1].strip().strip("[]")
            ucs = ucs_str.replace("'", "").split(", ")
            data.append({"Date": datetime_str, "UCs": len(ucs), "Config": current_config})
        if "finalizada" in line:
            parts = line.split(' ')
            datetime_str = ' '.join(parts[:2])  # A data e hora estão no início da linha
            uc_number = parts[3]
            ucs_data.append({"Date": datetime_str, "UC": uc_number, "Config": current_config})

    # Verificação se data não está vazia
    if not data:
        data.append({"Date": None, "UCs": 0, "Config": None})
    
    df = pd.DataFrame(data)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')  # Converter a coluna DateTime para o formato datetime
        df = df.groupby(['Date', 'Config']).sum().reset_index()

    ucs_df = pd.DataFrame(ucs_data)
    if not ucs_df.empty:
        ucs_df['Date'] = pd.to_datetime(ucs_df['Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

    return df, ucs_df

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
        
         # Criar o diretório, caso não exista
        criar_pasta_excel()
        
        # Gerar o arquivo Excel usando a função exportar_para_excel
        caminho_arquivo_excel = os.path.join(CAMINHO_EXCEL, 'dados_tms.xlsx')
        exportar_para_excel(tms_lista=telemetrias, caminho_arquivo_excel=caminho_arquivo_excel)
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

@app.route('/dashboards/data')
def dashboard_data():
    df, _ = read_log()
    fig = px.bar(df, x="Date", y="UCs", color="Config", title="Histograma de UCs por Configuração e Dia")
    graphJSON = fig.to_json()
    return jsonify(graphJSON)

@app.route('/dashboards/table_data')
def dashboard_table_data():
    df, _ = read_log()
    table_data = df.to_dict(orient='records')
    return jsonify(table_data)

@app.route('/dashboards/uc_data')
def dashboard_uc_data():
    _, ucs_df = read_log()
    uc_data = ucs_df.to_dict(orient='records')
    return jsonify(uc_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
