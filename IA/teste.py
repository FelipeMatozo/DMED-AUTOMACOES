from ReconhecimentoDeImagem import Reconhecimento

rec = Reconhecimento(numeroDeTentativasMax=5, delay=0.7)
rec.localizar_palavra_rolando("0172", max_tentativas=20, scroll_pixels=-175)
# rec.localiza("0172", 0.7)
