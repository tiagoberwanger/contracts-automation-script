from src.auth import documento_id_com_dados_inquilinos
from utils import abrir_planilha, formatar_dados, substituir_dados, alterar_status_contratos_gerados, obter_valores_de_planilha, enviar_email_com_contrato, \
    converter_contrato_para_pdf


def main():
    # abre planilha com dados de inquilinos
    planilha = abrir_planilha(chave=documento_id_com_dados_inquilinos)
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

        # coleta e formata dados
        dados_formatados = formatar_dados(dados_apresentados)

        # substitui dados formatados no contrato
        documento_id = substituir_dados(dados_formatados)

        # transformar contrato em PDF
        arquivo_em_bytes = converter_contrato_para_pdf(documento_id)

        # envia rascunho por e-mail para eu conferir
        enviar_email_com_contrato(dados_formatados.get('nome'), arquivo_em_bytes)

    # altera status do contrato gerado
    alterar_status_contratos_gerados()

if __name__ == '__main__':
    main()

# DONE Pesquisar como fazer um script em py
# DONE Criar um formulário para o usuário inserir esses dados (google forms)
# DONE Usar API do sheets para acessar planilha com dados dos inquilinos do formulário do sheets
# DONE Pesquisar libs para manipular .docx
# DONE Manipular as informações do .docx, buscar e substitui palavras-chave, entregar o documento formatado
# DONE Formatar CPF na saída, ajustar data por extenso e data do contrato
# DONE Usar APIs do google (drive, sheets, docs)
# DONE Ao salvar, mudar o status do contrato realizado
# TODO Eliminar o gspread
# TODO Salvar chaves no .env
# DONE Salvar, após concluído, esse contrato em formato PDF
# DONE Enviar, após preenchido, esse contrato para o meu e-mail para conferência
