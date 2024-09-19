'''
Este programa permite ao usuário buscar as 5 antenas mais próximas de uma (UC) específica no estado do Paraná.
Ele utiliza dados de localização das UCs e das antenas, sendo esses dados lidos de arquivos CSV e Excel, respectivamente.
Ao inserir o número de uma UC e clicar no botão "Buscar", o programa calcula as distâncias entre essa UC e todas as antenas listadas, encontrando as 5 antenas mais próximas.
Em seguida, ele exibe um mapa interativo usando a biblioteca Folium, mostrando a localização da UC, das antenas próximas e as linhas que as conectam.
Além disso, o mapa também apresenta uma legenda colorida indicando as operadoras das antenas (TIM, Claro, Vivo, Sercomtel) e a distância até a UC em quilômetros.
Após gerar o mapa, ele é salvo como um arquivo HTML e aberto automaticamente em um navegador web.
'''
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
from folium import MacroElement


# Adiciona o caminho do diretório principal (SISTEMA_RPA_DMED) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_dir = os.path.dirname(os.path.abspath(__file__))
script_cor = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from apps.utils import strings
from apps.utils.banco_utils import buscar_dados, buscar_todos_dados, ver_exist



def buscar_lat_lon(uc):
    resultado = buscar_dados("UC_LAT_LONG", "UC", uc, ["LATITUDE", "LONGITUDE"])
    
    if resultado:
        latitude, longitude = resultado
        return float(latitude), float(longitude)
        
    else:
        return None


# Encontra as 5 antenas mais próximas da UC dada
def encontrar_antenas_mais_proximas(uc_lat, uc_lon, n=5, threshold_dist=0.008, offset=0.00002):
    # Buscar todas as antenas da tabela antenas_parana
    colunas = ["latitude_antena", "longitude_antena", "operadora"]
    antenas = buscar_todos_dados("antenas_parana", colunas)

    distancias_antenas = []
    
    # Calcular as distâncias entre a UC e as antenas
    for antena_lat, antena_lon, operadora in antenas:
        distancia = geodesic((uc_lat, uc_lon), (antena_lat, antena_lon)).kilometers
        distancias_antenas.append((distancia, (antena_lat, antena_lon, operadora, distancia)))

    # Usa a função "nsmallest" que busca as N antenas com as menores distâncias da UC
    antenas_mais_proximas = nsmallest(n, distancias_antenas, key=lambda x: x[0])
    
    # Adiciona pequenas diferenças às coordenadas das antenas mais próximas apenas se estiverem muito próximas
    for i in range(1, len(antenas_mais_proximas)):
        lat_anterior, lon_anterior = antenas_mais_proximas[i-1][1][0], antenas_mais_proximas[i-1][1][1]
        lat_atual, lon_atual = antenas_mais_proximas[i][1][0], antenas_mais_proximas[i][1][1]
        
        distancia_entre_antenas = geodesic((lat_anterior, lon_anterior), (lat_atual, lon_atual)).kilometers
        
        if distancia_entre_antenas < threshold_dist:
            antenas_mais_proximas[i] = (
                antenas_mais_proximas[i][0], 
                (lat_atual + (i * 0.00002), lon_atual + (i * offset), antenas_mais_proximas[i][1][2], antenas_mais_proximas[i][1][3])
            )
        
    return [antena[1] for antena in antenas_mais_proximas]

def calcular_ponto_medio(lat1, lon1, lat2, lon2):
    """Calcula um ponto médio aproximado entre dois pontos geográficos."""
    lat_medio = (lat1 + lat2) / 2
    lon_medio = (lon1 + lon2) / 2
    return lat_medio, lon_medio

# Função para lidar com o botão "Buscar"
def buscar(numero_uc):

    if ver_exist("UC_LAT_LONG","UC", numero_uc) == True:
        print(f'A UC: {numero_uc} está presente no banco de dados!')

        latitude_uc, longitude_uc = buscar_lat_lon(numero_uc)

        if latitude_uc is not None and longitude_uc is not None:
            antenas_proximas = encontrar_antenas_mais_proximas(latitude_uc, longitude_uc)
            
            if antenas_proximas:
                parana_map = folium.Map(location=[latitude_uc, longitude_uc], zoom_start=16, height='95%')

                for antena in antenas_proximas:
                    distancia_km = antena[3]
                    popup_text = f"Operadora: {antena[2]}\nDistância até a UC: {distancia_km:.2f} km"
                    folium.Marker((antena[0], antena[1]), popup=popup_text, icon=folium.Icon(color='blue')).add_to(parana_map)

                folium.Marker([latitude_uc, longitude_uc], popup=f'UC: {numero_uc}', icon=folium.Icon(color='green')).add_to(parana_map)

                cores_operadoras = {'Tim': 'blue', 'Claro': 'red', 'Vivo': 'purple', 'Sercomtel': 'orange'}

                for antena in antenas_proximas:
                    distancia_km = antena[3]
                    operadora = antena[2]
                    lat_antena = antena[0]
                    lon_antena = antena[1]
                    cor_icone = cores_operadoras.get(operadora, 'gray')
                    popup_text = (
                        f"Operadora: {operadora}\n"
                        f"Distância até a UC: {distancia_km:.2f} km\n"
                        f"Latitude: {lat_antena:.6f}\n"
                        f"Longitude: {lon_antena:.6f}"
                    )
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
            
                # Defina o caminho do diretório e do arquivo
                directory = os.path.join(script_cor,'assets', 'html')
                mapa = os.path.join(directory, f'mapa_{numero_uc}.html')

                # Verifique se o diretório existe; se não, crie-o
                if not os.path.exists(directory):
                    os.makedirs(directory)
                print(directory)
                # Salvar o mapa como um arquivo HTML
                parana_map.save(mapa)
    else:
        print(f'A UC: {numero_uc} NÃO está presente no banco de dados!')

if __name__ == '__main__':
    buscar(1937340)
