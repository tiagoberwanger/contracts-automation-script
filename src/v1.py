from utils import data_por_extenso, substituir_dados, valor_formatado_por_extenso

novo_contrato = input('É um novo contrato? (S ou N):')
eh_novo_contrato = True if novo_contrato == 'S' else False

tipo_imovel = None
cpf = None
nacionalidade = None
naturalidade = None
estado_civil = None
numero = None
data_entrada = None
data_entrada_por_extenso = None
data_saida = None
data_saida_por_extenso = None
valor_formatado = None
valor_por_extenso = None
data_da_assinatura = None

if eh_novo_contrato:
    nome = input('Digite o nome do inquilino:')
    cpf = input('Digite o CPF do inquilino (formato ___.___.___.___.___):')
    nacionalidade = input('Digite sua nacionalidade:')
    naturalidade = input('Digite em qual cidade e estado você é natural (formato _______/__):')
    estado_civil = input('Digite seu estado civil:')
    tipo_imovel = input('Digite o tipo do imóvel (quarto, quitinete ou apartamento):')
    numero = input('Digite o número do imóvel:')
    data_entrada = input('Digite a data de entrada/início da vigência do contrato (formato __/__/____):')
    data_entrada_por_extenso = data_por_extenso(data_entrada)
    data_saida = input('Digite a data de saída/fim da vigência do contrato (formato __/__/____):')
    data_saida_por_extenso = data_por_extenso(data_saida)
    valor = input('Digite o valor do aluguel (apenas números):')
    valor_formatado = f'R$ {valor},00'
    valor_por_extenso = valor_formatado_por_extenso(valor)
    data_da_assinatura = input('Digite a data da assinatura (formato __/__/____):')
else:
    nome = input('Digite o nome do inquilino que você quer renovar o contrato:')
    # TODO Separar novos contratos de renovações
    print('Recurso não disponível!')

# TODO Validação dos inputs e verificação de dados presentes

dados_alterar_renovacao = {
    '{numero}': numero,
    '{data_entrada}': data_entrada,
    '{data_entrada_por_extenso}': data_entrada_por_extenso,
    '{data_saida}': data_saida,
    '{data_saida_por_extenso}': data_saida_por_extenso,
    '{valor}': valor_formatado,
    '{valor_por_extenso}': valor_por_extenso,
    '{data_da_assinatura}': data_da_assinatura
}

dados_alterar_novo = {
    **dados_alterar_renovacao,
    '{nome}': nome.upper(),
    '{cpf}': cpf,
    '{nacionalidade}': nacionalidade,
    '{naturalidade}': naturalidade,
    '{estado_civil}': estado_civil,
}


eh_novo = True
dados = dados_alterar_novo if eh_novo else dados_alterar_renovacao

# Substitui o texto pelas informações fornecidas
substituir_dados(dados)
