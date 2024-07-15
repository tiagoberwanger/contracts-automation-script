from utils import abrir_planilha, formatar_dados, substituir_dados, alterar_status_contrato


def main():
    planilha = abrir_planilha(chave='1UzHWKA-qZTEfPDXs1l4o7FUp3BuI-MZcU3aEqYYJCbo')
    dados = planilha.get_all_values()

    chave = dados[1]
    valores = dados[2:]

    for valor in valores:
        contrato_foi_gerado = valor[-1] == 'TRUE'
        if contrato_foi_gerado:
            continue

        dados_apresentados = {}
        for c, v in zip(chave, valor):
            dados_apresentados[c] = v

        dados_formatados = formatar_dados(dados_apresentados)

        substituir_dados(dados_formatados)

        alterar_status_contrato()


if __name__ == '__main__':
    main()

# DONE Pesquisar como fazer um script em py
# DONE Criar um formulário para o usuário inserir esses dados (google forms)
# DONE Usar API do sheets para acessar planilha com dados dos inquilinos do formulário do sheets
# DONE Pesquisar libs para manipular .docx
# DONE Manipular as informações do .docx, buscar e substitui palavras-chave, entregar o documento formatado
# TODO Ao salvar, mudar o status do contrato realizado
# TODO Salvar, após concluído, esse contrato em formato PDF
# TODO Enviar, após preenchido, esse contrato para o e-mail do inquilino
