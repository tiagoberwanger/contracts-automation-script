from num2words import num2words

def valor_formatado_por_extenso(numero):
    valor_por_extenso = num2words(numero, lang='pt_BR')
    return f'{valor_por_extenso} reais'


def data_por_extenso(data):
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