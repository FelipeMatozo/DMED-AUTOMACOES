from ReconhecimentoDeImagem import Reconhecimento

start = Reconhecimento(numeroDeTentativasMax=5, delay=0.7)

# start.localizar_palavra_rolando("E750 G2", max_tentativas=20, scroll_pixels=1)
# start.localizar_palavra_rolando("75.16", max_tentativas=20, scroll_pixels=1)
start.localizar_palavra_rolando("CAPITÃO LEÔNIDAS MARQUES TESTA", max_tentativas=20, scroll_pixels=100)