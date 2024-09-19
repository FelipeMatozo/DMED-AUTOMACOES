# Mensagens de boas-vindas
welcome_message = "Bem vindo ao Centro de Operções da Medição da COPEL distribuição\nPor favor, escolha uma das opções abaixo:"
help_message = "Aqui estão os comandos disponíveis:\n/start - Inicia a interação com o bot\n/help - Mostra esta mensagem de ajuda"
nenhuma = "Nenhuma telemetria encontrada"
#botoes do menu
botao1 = "Telemetria"
botao2 = "Medidor"
botao3 = "Cobertura de Sinal"
botao4 = "Ajuda"
#statusdousuario
statusTele1 = "Tele1"
statusTele2 = "Tele2"
statusOut = "Voltar"
statusmenu3info1 = "mapa"
# Mensagens do submenu
msgsubmenu1 = "Selecione o teste de comunicação."
msgsubmenu2 = "Acesse as opções do Medidor para gerenciar e analisar os dados coletados."
msgsubmenu3 = "Gerar mapa"
msgsubmenu4 = "Precisa de suporte técnico? Estamos prontos para ajudar com qualquer dúvida ou problema técnico."

#botoes menu1
tele1 = "Verificar Status"
tele2 = "Comissionamento"
#botoes menu 3
menu3info1 = "Antenas próximas da uc"
menu3info2 = "Operadoras na regiao"
#botoes menu 2
menu2info1 = "Memória de massa"
menu2info2 = "Ajuste de Relógio"
#botoes menu 4
menu4info1 = "Fala com a central"
menu4info2 = "Sair"
#botoes do submenu telemtria
menutele = "Escolha o procedimento:"

# Opções do menu
clientes_livres = "Verificar Status Telemetria clientes livres"
consultar_uc = "Consultar UC"
consultar_nio = "Consultar NIO"

# Mensagens de erro
input_error = "Por favor, insira um número que comece com '00' seguido por exatamente oito dígitos inteiros"
inputUC_error = "Por favor, insira um número que tenha exatamente oito dígitos inteiros"
naoDisponivel = "Função não disponível"
spam = "Você atingiu o limite de mensagens. Por favor, aguarde 30 segundos."
intError = 'Por favor, insira apenas números inteiros.'
uc_input_error = 'Por favor, insira apenas números com no máximo 10 digitos'
UC_404 = 'Unidade consumidora Inexistente'




header = """
            {% macro html(this, kwargs) %} 
<div class="container-fluid" style="position: fixed; top: 0; width: 100%; height: 5em; background-color: #8b7d6b; color: white; border-bottom: 2px solid #4d4d4d; z-index: 9999; display: flex; align-items: center; justify-content: center;">
    <div>
        <div class="text-center" style="font-size: 24px;">
            <strong>Departamento de Medição</strong>
        </div>
    </div>
</div>
{% endmacro %}
"""



header = """
            {% macro html(this, kwargs) %} 
<div class="container-fluid" style="position: fixed; top: 0; width: 100%; height: 5em; background-color: #ACA192; color: white; border-bottom: 2px solid #4d4d4d; z-index: 9999; display: flex; align-items: center; justify-content: center;">
    <div>
        <div class="text-center" style="font-size: 24px;">
            <strong>Departamento de Medição</strong>
        </div>
    </div>
</div>
{% endmacro %}
"""

footer = """
{% macro html(this, kwargs) %}
<div class="container">
    <div class="row">
        <div class="col text-center">
            <span>UC</span> <i class="fa fa-map-marker" style="color:green;"></i>
        </div>
        <div class="col text-center">
            <span>TIM</span> <i class="fa fa-map-marker" style="color:DodgerBlue;"></i>
        </div>
        <div class="col text-center">
            <span>CLARO</span> <i class="fa fa-map-marker" style="color:red;"></i>
        </div>
        <div class="col text-center">
            <span>VIVO</span> <i class="fa fa-map-marker" style="color:purple;"></i>
        </div>
        <div class="col text-center">
            <span>SERCOMTEL</span> <i class="fa fa-map-marker" style="color:orange;"></i>
        </div>
    </div>
</div>
{% endmacro %}
"""

