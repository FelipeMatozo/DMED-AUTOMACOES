
# Encurta o texto, pulando a primeira palavra e mantendo as próximas duas
texto_nome_ponto= "SE BANCO DO BRA33333SILretertert COPEL ROCKEFELLER - ENTRADA 1 13,8 KV"

palavras = texto_nome_ponto.split()  # Divide o texto em palavras

if len(palavras) > 4:
    texto_encurtado = " ".join(palavras[1:4])  # Pula a primeira palavra e pega as próximas duas
elif len(palavras) == 4:
    texto_encurtado = " ".join(palavras[1:])  # Pega a segunda palavra se houver apenas duas
else:
    texto_encurtado = ""  # Se houver apenas uma palavra ou nenhuma

# Limita o texto encurtado a 15 caracteres
if len(texto_encurtado) > 15:
    texto_encurtado = texto_encurtado[:15]  # Trunca o texto para 15 caracteres

    # Se a última palavra estiver sendo truncada, continua removendo até que esteja dentro do limite
    while len(texto_encurtado) > 15:
        # Encontra a última palavra e a reduz em um caractere
        palavras_espacos = texto_encurtado.rsplit(' ', 1)  # Divide em duas partes na última ocorrência de espaço
        if len(palavras_espacos) == 2:
            texto_encurtado = f"{palavras_espacos[0]} {palavras_espacos[1][:-1]}"
        else:
            texto_encurtado = palavras_espacos[0][:-1]  # Remove um caractere se só houver uma palavra

print(f'Texto encurtado do campo "nomePontoMedicao": "{texto_encurtado}"')