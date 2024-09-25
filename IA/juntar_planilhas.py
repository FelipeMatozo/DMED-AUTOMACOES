import pandas as pd

# Lista de arquivos Excel a serem combinados (com caminho corrigido)
files = ['assets\\excel\\Final_sinal_op\\final_Oi_Livres.xlsx', 
         'assets\\excel\\Final_sinal_op\\final_TIM_Livres.xlsx', 
         'assets\\excel\\Final_sinal_op\\final_Vivo_Livres.xlsx']

# Lista para armazenar os dataframes de cada planilha
dataframes = []

# Loop para ler cada arquivo Excel e adicionar à lista de dataframes
for file in files:
    df = pd.read_excel(file)
    dataframes.append(df)

# Concatenar todos os dataframes em um único
combined_df = pd.concat(dataframes, ignore_index=True)

# Salvar o dataframe combinado em um novo arquivo Excel
combined_df.to_excel('assets\\excel\\Final_sinal_op\\combined_planilha.xlsx', index=False)

print("Planilhas combinadas com sucesso em 'combined_planilha.xlsx'")
