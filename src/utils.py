from num2words import num2words
from datetime import date

from enums import TipoImovelEnum

ANO_ATUAL = date.today().year


def valor_formatado_por_extenso(numero: int):
    valor_por_extenso = num2words(numero, lang='pt_BR')
    return f'{valor_por_extenso} reais'


def data_por_extenso(data: str):
    dia, mes, ano = map(int, data.split('/'))

    dia_extenso = num2words(dia, lang='pt_BR', to='ordinal')
    ano_extenso = num2words(ano, lang='pt_BR', to='year')

    meses = [
        'janeiro', 'fevereiro', 'março', 'abril',
        'maio', 'junho', 'julho', 'agosto',
        'setembro', 'outubro', 'novembro', 'dezembro'
    ]
    mes_extenso = meses[mes - 1]

    return f"{dia_extenso} de {mes_extenso} de {ano_extenso}"


def abrir_planilha(chave: str):
    import gspread

    gc = gspread.service_account('/Users/mplayer/Developer/quickstart-google-api/.config/gspread/service_account.json')

    sheet = gc.open_by_key(chave)

    return sheet.get_worksheet(0)


def alterar_status_contrato():
    pass


def obtem_valor_por_tipo_imovel(tipo_imovel: int):
    VALORES = {
        TipoImovelEnum.QUITINETE: 800,
        TipoImovelEnum.APARTAMENTO: 1200,
        TipoImovelEnum.QUARTO: 400
    }
    return VALORES.get(tipo_imovel, 0)


def formatar_dados(dados: dict):
    nome_formatado = dados.get('nome').upper()
    data_entrada = dados.get('data_entrada')
    tipo_imovel = dados.get('tipo_imovel')[0]
    valor = obtem_valor_por_tipo_imovel(int(tipo_imovel))
    valor_por_extenso = valor_formatado_por_extenso(valor)
    data_saida = data_entrada.replace(data_entrada.split('/')[2], str(date.today().year + 1))
    data_hoje = date.today().strftime('%d/%m/%Y')

    return {
        'nome': nome_formatado,
        'tipo_imovel': int(tipo_imovel),
        'cpf': dados.get('cpf'),
        'nacionalidade': dados.get('nacionalidade'),
        'naturalidade': dados.get('naturalidade'),
        'estado_civil': dados.get('estado_civil'),
        'numero': dados.get('numero_imovel'),
        'data_entrada': data_entrada,
        'data_entrada_por_extenso': data_por_extenso(data_entrada),
        'data_saida': data_saida,
        'data_saida_por_extenso': data_por_extenso(data_saida),
        'valor': f'R$ {str(valor)},00',
        'valor_por_extenso': valor_por_extenso,
        'data_da_assinatura': data_hoje
    }


def substituir_dados(dados: dict):
    from docx import Document

    # Define qual o contrato
    CONTRATO_POR_IMOVEL = {
        TipoImovelEnum.QUITINETE: 'contrato_quitinete',
        TipoImovelEnum.APARTAMENTO: 'contrato_apartamento',
        TipoImovelEnum.QUARTO: 'contrato_quarto'
    }
    contrato = CONTRATO_POR_IMOVEL[dados.get('tipo_imovel')]
    documento_contrato = Document(f'./contratos/{contrato}_modelo.docx')

    dados_alterar_novo = {
        '{nome}': dados.get('nome'),
        '{cpf}': dados.get('cpf'),
        '{nacionalidade}': dados.get('nacionalidade'),
        '{naturalidade}': dados.get('naturalidade'),
        '{estado_civil}': dados.get('estado_civil'),
        '{numero}': dados.get('numero'),
        '{data_entrada}': dados.get('data_entrada'),
        '{data_entrada_por_extenso}': dados.get('data_entrada_por_extenso'),
        '{data_saida}': dados.get('data_saida'),
        '{data_saida_por_extenso}': dados.get('data_saida_por_extenso'),
        '{valor}': dados.get('valor'),
        '{valor_por_extenso}': dados.get('valor_por_extenso'),
        '{data_da_assinatura}': dados.get('data_da_assinatura')
    }

    try:
        for p in documento_contrato.paragraphs:
            for k, v in dados_alterar_novo.items():
                if k in p.text:
                    p.text = p.text.replace(k, v)

        # Salva o documento modificado
        nome_formatado = dados.get('nome').replace(' ', '_').lower()
        documento_contrato.save(f'./contratos/{contrato}_{nome_formatado}_{ANO_ATUAL}.docx')

        # Mensagem de sucesso
        print("Novo contrato criado com sucesso!")

    except Exception as e:
        print(e)
        print("Não foi possível salvar o contrato!")
