from auth import documento_id_com_dados_inquilinos
from utils import abrir_planilha, formatar_dados, substituir_dados, alterar_status_contratos_gerados, obter_valores_de_planilha, enviar_email_com_contrato, \
    converter_contrato_para_pdf


def contract_task():
    print('Pesquisando contratos')
    # abre planilha com dados de inquilinos
    planilha = abrir_planilha(documento_id=documento_id_com_dados_inquilinos, range="A2:L50")
    chave, valores = obter_valores_de_planilha(planilha)

    # verifica se há contratos para gerar
    todos_os_contratos_foram_gerados = all(valor[-1] == 'TRUE' for valor in valores)
    if todos_os_contratos_foram_gerados:
        print('Todos os contratos já foram gerados!')
        return

    # itera sobre valores de cada contrato
    for valor in valores:
        contrato_foi_gerado = valor[-1] == 'TRUE'
        if contrato_foi_gerado:
            continue

        dados_apresentados = {}
        for c, v in zip(chave, valor):
            dados_apresentados[c] = v

        # iniciando processo
        print('Iniciando contrato...')

        # coleta e formata dados
        dados_formatados = formatar_dados(dados_apresentados)

        # substitui dados formatados no contrato
        documento_id = substituir_dados(dados_formatados)

        # transformar contrato em PDF
        arquivo_em_bytes = converter_contrato_para_pdf(documento_id)

        # envia rascunho por e-mail para eu conferir
        dados_envio = {
            'nome': dados_apresentados.get('nome'),
            'email': dados_apresentados.get('email')
        }
        enviar_email_com_contrato(dados_envio, arquivo_em_bytes)

    # altera status do contrato gerado
    alterar_status_contratos_gerados()

if __name__ == '__main__':
    contract_task()
