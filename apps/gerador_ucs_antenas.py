from folium import IFrame
import os
import sys
from os.path import basename
import csv
import pandas as pd
import folium
import webbrowser
from geopy.distance import geodesic
from heapq import nsmallest
from branca.element import Template, MacroElement
from folium.plugins import FloatImage
from folium.features import DivIcon
import utils.strings as strings
import sqlite3

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Caminho da lista de UC's com as localizações
LocCsv = get_resource_path('RPA_buscador/csv/loc_uc.csv')
antenas = get_resource_path('RPA_buscador/csv/antenas_parana.csv')
banco = get_resource_path('Banco/banco_dmed')

# Ler os arquivos CSV
data = pd.read_csv(antenas)

def verificar_banco(numero_uc):
    # Conectar ao banco de dados
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    # Verificar se a UC existe na tabela UC_LAT_LONG
    cursor.execute("SELECT COUNT(*) FROM UC_LAT_LONG WHERE UC = ?", (numero_uc,))
    resultado = cursor.fetchone()[0]

    # Fechar a conexão com o banco de dados
    conexao.close()

    # Retornar True se a UC existir, False caso contrário
    return resultado > 0

# Função que pega a UC dada pelo usuário e acha a latitude e a longitude correspondente na lista de UC's
def buscar_lat_lon(uc):
    # Conectar ao banco de dados
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    # Consultar a latitude e a longitude da tabela UC_LAT_LONG
    cursor.execute("SELECT LATITUDE, LONGITUDE FROM UC_LAT_LONG WHERE UC = ?", (uc,))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    conexao.close()

    # Verificar se a consulta retornou um resultado
    if resultado:
        latitude, longitude = resultado
        return float(latitude), float(longitude)
    else:
        # Retornar None ou lançar uma exceção se a UC não for encontrada
        return None

# Encontra as 5 antenas mais próximas da UC dada
def encontrar_antenas_mais_proximas(uc_lat, uc_lon, data, n=5):
    distancias_antenas = []
    
    for index, row in data.iterrows():
        antena_lat = float(row['latitude_antena'])
        antena_lon = float(row['longitude_antena'])
        distancia = geodesic((uc_lat, uc_lon), (antena_lat, antena_lon)).kilometers
        distancias_antenas.append((distancia, (antena_lat, antena_lon, row['operadora'], distancia)))

    # Usa a função "nsmallest" que busca as 5 antenas com as menores distâncias da UC
    antenas_mais_proximas = nsmallest(n, distancias_antenas, key=lambda x: x[0])
    
    # Adiciona pequenas diferenças às coordenadas das antenas mais próximas
    for i, antena in enumerate(antenas_mais_proximas):
        lat, lon, operadora, distancia = antena[1]
        lat += (i * 0.00007)  # Adiciona uma pequena diferença na latitude
        lon += (i * 0.00007)  # Adiciona uma pequena diferença na longitude
        antenas_mais_proximas[i] = (antena[0], (lat, lon, operadora, distancia))
        
    return [antena[1] for antena in antenas_mais_proximas]

def calcular_ponto_medio(lat1, lon1, lat2, lon2):
    """Calcula um ponto médio aproximado entre dois pontos geográficos."""
    lat_medio = (lat1 + lat2) / 2
    lon_medio = (lon1 + lon2) / 2
    return lat_medio, lon_medio

# Função para lidar com o botão "Buscar"
def buscar(numero_uc):
    print(numero_uc)
    latitude_uc, longitude_uc = buscar_lat_lon(numero_uc)

    if latitude_uc is not None and longitude_uc is not None:
        antenas_proximas = encontrar_antenas_mais_proximas(latitude_uc, longitude_uc, data)
        
        if antenas_proximas:
            parana_map = folium.Map(location=[latitude_uc, longitude_uc], zoom_start=14, height='95%')

            for antena in antenas_proximas:
                distancia_km = antena[3]
                popup_text = f"Operadora: {antena[2]}\nDistância até a UC: {distancia_km:.2f} km"
                folium.Marker((antena[0], antena[1]), popup=popup_text, icon=folium.Icon(color='blue')).add_to(parana_map)

            folium.Marker([latitude_uc, longitude_uc], popup=f'UC: {numero_uc}', icon=folium.Icon(color='green')).add_to(parana_map)

            cores_operadoras = {'Tim': 'blue', 'Claro': 'red', 'Vivo': 'purple', 'Sercomtel': 'orange'}

            for antena in antenas_proximas:
                distancia_km = antena[3]
                operadora = antena[2]
                cor_icone = cores_operadoras.get(operadora, 'gray')
                popup_text = f"Operadora: {operadora}\nDistância até a UC: {distancia_km:.2f} km"
                folium.Marker((antena[0], antena[1]), popup=popup_text, icon=folium.Icon(color=cor_icone)).add_to(parana_map)

            for antena in antenas_proximas:
                folium.PolyLine(locations=[(latitude_uc, longitude_uc), (antena[0], antena[1])], color='red').add_to(parana_map)
                ponto_medio_lat, ponto_medio_lon = calcular_ponto_medio(latitude_uc, longitude_uc, antena[0], antena[1])
                distancia_km = antena[3]
                texto_distancia = f"{distancia_km:.2f} km"
                folium.map.Marker((ponto_medio_lat, ponto_medio_lon), icon=DivIcon(icon_size=(150, 36), icon_anchor=(0, 0), html=f'<div style="font-size: 24px; font-weight: bold">{texto_distancia}</div>')).add_to(parana_map)

            # Adicionar o cabeçalho HTML personalizado
            macro_header = MacroElement()
            macro_header._template = Template(strings.header)
            parana_map.get_root().add_child(macro_header)

            # Adicionar o rodapé HTML personalizado (legenda de cores)
            macro_footer = MacroElement()
            macro_footer._template = Template(strings.footer)
            parana_map.get_root().add_child(macro_footer)

            # Salvar o mapa como um arquivo HTML com o nome especificado,
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            mapa = os.path.join(parent_dir, 'assets', 'html', f'mapa_{numero_uc}.html')
            parana_map.save(mapa)

if __name__ == '__main__':
    buscar(19452241)
