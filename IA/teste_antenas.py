import os
import sys
import pandas as pd
from geopy.distance import geodesic
from heapq import nsmallest
from banco_utils import buscar_dados, buscar_todos_dados, ver_exist

# Adiciona o caminho do diretório principal (SISTEMA_RPA_DMED) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def buscar_lat_lon(uc):
    resultado = buscar_dados("UC_LAT_LONG", "UC", uc, ["LATITUDE", "LONGITUDE"])
    
    if resultado:
        latitude, longitude = resultado
        return float(latitude), float(longitude)
    else:
        return None

# Encontra as 3 antenas mais próximas da UC dada
def encontrar_antenas_mais_proximas(uc_lat, uc_lon, n=3):
    colunas = ["latitude_antena", "longitude_antena", "operadora", "estacao"]  # Inclui "estacao"
    antenas = buscar_todos_dados("antenas_parana", colunas)

    distancias_antenas = []
    
    # Calcular as distâncias entre a UC e as antenas
    for antena_lat, antena_lon, operadora, estacao in antenas:  # Inclui "estacao"
        distancia = geodesic((uc_lat, uc_lon), (antena_lat, antena_lon)).kilometers
        distancias_antenas.append((distancia, (operadora, estacao)))  # Guarda operadora e estacao

    # Usa a função "nsmallest" que busca as N antenas com as menores distâncias da UC
    antenas_mais_proximas = nsmallest(n, distancias_antenas, key=lambda x: x[0])
    
    return [
        (antena[1][0], antena[1][1], f"{antena[0]:.2f} km")  # Adiciona "km" à distância
        for antena in antenas_mais_proximas
    ]

# Função para lidar com o botão "Buscar"
def buscar(numero_uc):
    if ver_exist("UC_LAT_LONG", "UC", numero_uc):
        print(f'A UC: {numero_uc} está presente no banco de dados!')

        latitude_uc, longitude_uc = buscar_lat_lon(numero_uc)

        if latitude_uc is not None and longitude_uc is not None:
            antenas_proximas = encontrar_antenas_mais_proximas(latitude_uc, longitude_uc)

            if antenas_proximas:
                # Separar os dados em colunas
                dados_formatados = {
                    "Antena 1": [f"{antenas_proximas[0][0]} ({antenas_proximas[0][1]})"],
                    "Distancia 1": [antenas_proximas[0][2]],
                    "Antena 2": [f"{antenas_proximas[1][0]} ({antenas_proximas[1][1]})"],
                    "Distancia 2": [antenas_proximas[1][2]],
                    "Antena 3": [f"{antenas_proximas[2][0]} ({antenas_proximas[2][1]})"],
                    "Distancia 3": [antenas_proximas[2][2]],
                }

                # Criar um DataFrame com os dados formatados
                df = pd.DataFrame(dados_formatados)

                caminho_planilha = os.path.join('assets', 'excel', f'antenas_proximas_uc_{numero_uc}.xlsx')

                # Verificar se o diretório existe; se não, crie-o
                os.makedirs(os.path.dirname(caminho_planilha), exist_ok=True)

                # Salvar a planilha como um arquivo Excel
                df.to_excel(caminho_planilha, index=False)
                print(f'Planilha criada: {caminho_planilha}')
            else:
                print("Nenhuma antena encontrada próxima à UC.")
    else:
        print(f'A UC: {numero_uc} NÃO está presente no banco de dados!')

if __name__ == '__main__':
    buscar(1937340)
