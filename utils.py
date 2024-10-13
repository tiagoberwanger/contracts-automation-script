import base64
from collections.abc import Callable
from email.message import EmailMessage

from googleapiclient.errors import HttpError
from num2words import num2words
from datetime import date

from enums import TipoImovelEnum
from auth import get_authenticated_service, documento_id_com_dados_inquilinos

DATA_HOJE = date.today()
ANO_ATUAL = DATA_HOJE.year
MES_ATUAL = DATA_HOJE.month
DIA_ATUAL = DATA_HOJE.day
MESES = [
    'janeiro', 'fevereiro', 'março', 'abril',
    'maio', 'junho', 'julho', 'agosto',
    'setembro', 'outubro', 'novembro', 'dezembro'
]


def valor_formatado_por_extenso(numero: int):
    valor_por_extenso = num2words(numero, lang='pt_BR')
    return f'{valor_por_extenso} reais'


def data_por_extenso(data: str):
    dia, mes, ano = map(int, data.split('/'))

    dia_extenso = num2words(dia, lang='pt_BR', to='cardinal')
    mes_extenso = MESES[mes - 1]
    ano_extenso = num2words(ano, lang='pt_BR', to='year')

    return f"{dia_extenso} de {mes_extenso} de {ano_extenso}"


def abrir_planilha(documento_id: str, range: str):
    try:
        sheets_service = get_authenticated_service('sheets', 'v4')
        return sheets_service.spreadsheets().values().get(spreadsheetId=documento_id, range=range).execute()
    except HttpError as error:
        print(f"Ocorreu um erro ao abrir a planilha: {error}")


def alterar_status_contratos_gerados():
    sheets_service = None
    try:
        sheets_service = get_authenticated_service('sheets', 'v4')
    except HttpError as error:
        print(f"Ocorreu um erro ao acessar as APIs: {error}")

    try:
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=documento_id_com_dados_inquilinos, body={'requests': [{
            "findReplace": {
                "find": 'FALSE',
                "replacement": 'TRUE',
                "allSheets": True,
            }
        }]}).execute()

    except Exception as error:
        print(f"Ocorreu um erro ao alterar status do contrato gerado: {error}")


def _obter_valor_pelo_codigo_do_imovel(codigo_imovel: str):
    # legenda: número do imóvel (2 dígitos) + número de quartos (2 dígitos) + número do quarto (2 dígitos)
    VALOR_POR_CODIGO_IMOVEL = {
        '010100': 1050,
        '020100': 900,
        '030100': 900,
        '040100': 1050,
        '010200': 1350,
        '020200': 1250,
        '030200': 1100,
        '040301': 565,
        '040302': 450,
        '040303': 470,
        '050301': 480,
        '050302': 490,
        '050303': 490
    }
    return VALOR_POR_CODIGO_IMOVEL.get(codigo_imovel)


def formatar_cpf(cpf: str):
    if len(cpf) < 11:
        raise Exception('CPF incorreto!')
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'


def formatar_dados(dados: dict):
    nome_formatado = dados.get('nome').upper()
    cpf_formatado = formatar_cpf(dados.get('cpf'))
    data_entrada = dados.get('data_entrada')
    tipo_imovel = dados.get('tipo_imovel')[0]
    numero_formatado = str(dados.get('numero_imovel'))[:2]
    valor = _obter_valor_pelo_codigo_do_imovel(dados.get('numero_imovel'))
    valor_por_extenso = valor_formatado_por_extenso(valor)
    data_saida = data_entrada.replace(data_entrada.split('/')[2], str(date.today().year + 1))
    data_hoje = f'{DIA_ATUAL} de {MESES[MES_ATUAL - 1]} de {ANO_ATUAL}'
    valor_formatado = f'R${str(valor)},00'

    print('Formatando dados!')
    
    return {
        'nome': nome_formatado,
        'tipo_imovel': int(tipo_imovel),
        'cpf': cpf_formatado,
        'nacionalidade': dados.get('nacionalidade'),
        'naturalidade': dados.get('naturalidade'),
        'estado_civil': dados.get('estado_civil'),
        'numero': numero_formatado,
        'data_entrada': data_entrada,
        'data_entrada_por_extenso': data_por_extenso(data_entrada),
        'data_saida': data_saida,
        'data_saida_por_extenso': data_por_extenso(data_saida),
        'valor': valor_formatado,
        'valor_por_extenso': valor_por_extenso,
        'data_da_assinatura': data_hoje
    }


def obter_valores_de_planilha(planilha):
    dados = planilha.get("values", [])
    chave, valores = dados[0], dados[1:]
    return chave, valores


def substituir_dados(dados: dict):
    # Define qual o contrato
    CONTRATO_ID_POR_IMOVEL = {
        TipoImovelEnum.QUITINETE: '1hxLmEMkh_WrBqh0wgNUTvC6XDCKfdAt8',
        TipoImovelEnum.APARTAMENTO: '1Famz1SspXkRLKBYPWLf2xkTSo2HRjTOx',
        TipoImovelEnum.QUARTO: '1trCLTFo5bdRp7e-_Y6i1fpmJbbieGNFN'
    }
    modelo_id = CONTRATO_ID_POR_IMOVEL[dados.get('tipo_imovel')]

    del dados['tipo_imovel']

    # carregar serviços de APIs
    docs_service = None
    drive_service = None
    try:
        docs_service = get_authenticated_service('docs', 'v1')
        drive_service = get_authenticated_service('drive', 'v3')
    except HttpError as error:
        print(f"Ocorreu um erro ao acessar as APIs: {error}")

    # duplicar o modelo e salvar com a extensão do nome e timestamp (API drive)
    documento = drive_service.files().copy(fileId=modelo_id, body={'name': f"CONTRATO DE {dados.get('nome')}"}).execute()

    # iterar sobre tags e preencher com dados captados (API docs)
    lista_de_args = [k for k in dados.keys()]
    requests = []
    for arg in lista_de_args:
        tag = "{{" + str(arg) + "}}"
        texto = dados.get(arg)
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': tag,
                    'matchCase': 'true'
                },
                'replaceText': texto,
            },
        })

    try:
        docs_service.documents().batchUpdate(documentId=documento.get('id'), body={'requests': requests}).execute()
        print("Novo contrato criado!")
        return documento.get('id')

    except Exception as error:
        print(f"Ocorreu um erro ao criar o contrato: {error}")


def converter_contrato_para_pdf(documento_id: int):
    drive_service = None
    try:
        drive_service = get_authenticated_service('drive', 'v3')
    except HttpError as error:
        print(f"Ocorreu um erro ao acessar as APIs: {error}")

    try:
        arquivo_em_bytes = drive_service.files().export(fileId=documento_id, mimeType='application/pdf').execute()
        print("Arquivo em PDF exportado!")
        return arquivo_em_bytes
    except HttpError as error:
        print(f"Ocorreu um erro ao exportar o PDF: {error}")


def enviar_email_com_contrato(dados: dict, arquivo_em_bytes: bytes):
    gmail_service = None
    try:
        gmail_service = get_authenticated_service('gmail', 'v1')
    except HttpError as error:
        print(f"Ocorreu um erro ao acessar as APIs: {error}")

    try:
        mime_message = EmailMessage()

        # headers
        mime_message["From"] = "berwangertiago@gmail.com"
        mime_message["To"] = dados['email']
        mime_message["Subject"] = "Contrato de aluguel - Residencial"

        # text
        mime_message.set_content(
            f"Olá {dados['nome']}. Segue o seu contrato de aluguel em anexo! "
            "Favor ler com atenção e qualquer dúvida entrar em contato comigo. "
            "Att, Tiago."
        )

        mime_message.add_attachment(arquivo_em_bytes, 'application', 'pdf')

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_draft_request_body = {"message": {"raw": encoded_message}}
        gmail_service.users().drafts().create(userId="me", body=create_draft_request_body).execute()
        print("Contrato salvo nos rascunhos!")

    except Exception as error:
        print(f"Ocorreu um erro ao enviar o email: {error}")
