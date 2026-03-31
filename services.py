from datetime import date
from time import sleep
from datetime import datetime

VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
MAGENTA='\033[35m'
LARANJA='\033[38;5;208m'
CINZA='\033[90m'
RESET = '\033[0m'
NEGRITO = '\033[1m'
SUBLINHADO = '\033[4m'


info = {
    'nome': '',
    'salario': 0,
    'saldo':0,
    'valor_minimo':None,
    'despesas_fixas':[],
    'cartoes':[],
    'transacoes':[]
}

def erro_input():
    print(f"❌ Entrada inválida\n")
    sleep(0.2)  

def erro_opcao():
    print(f"❌ Opção inválida\n")
    sleep(0.2)

#Função para cadastro de nome do usuario
def cadastra_nome(info):
    while True:
        nome=input(f'Como gostaria de ser chamado(a)?: ').capitalize().strip()
        if not nome:
            print(f'⚠️ Favor informar dado solicitado')
            sleep(0.2)
        else:
            info['nome']=nome
            break
#Função para cadastro de valor mínimo a ser avisado sobre o saldo disponível
def cadastra_valor_minimo(info):
    try:
        while True:
            escolha=input(f"Gostaria de cadastrar um valor mínimo para alerta de saldo? [S/N]: ").lower().strip()
            if escolha == 's':
                valor_minimo=float(input(f"Informe o valor mínimo: R$"))
                if valor_minimo <=0:
                    print(f"⚠️ Informe um valor positivo e diferente de 0")
                    sleep(0.2)
                    continue
                else:
                    info['valor_minimo']= valor_minimo
                    return
            elif escolha=='n':
                info['valor_minimo']= None
                break 
            else:
                print(f"Informe S ou N")
                continue   
    except ValueError:
        erro_input()
        
#Função para cadastro de salário líquido
def cadastra_salario(info):
    try:
        while True:
            salario=float(input(f'Salário líquido mensal: R$'))
            if salario <=0:
                print(f'⚠️ Informar valor maior que 0!')
                sleep(0.2)
                continue
            else:
                info['salario']=salario
                info['saldo']+=salario
                break
        cadastra_valor_minimo(info)
    except ValueError:
        erro_input()

#Função para cadastro de gastos fixos
def cadastra_despesas_fixas(info):
    while True:
        try:
            descricao=input(f"Descrição: ").capitalize().strip()
            if not descricao:
                print(f"⚠️ Informação obrigatória!")
                sleep(0.2)
                continue
            valor=float(input(f"Valor: R$"))
            if valor <= 0:
                print(f"⚠️ Favor informar um valor válido!")
                sleep(0.2)
                continue
            info['despesas_fixas'].append({'descricao':descricao, 'valor':valor})
            registra_transacao(
                info,
                descricao=descricao,
                valor=-valor,
                tipo='saida',
                forma_pagamento='despesa_fixa'
            )
            while True:
                escolha=input(f"\nGostaria de cadastrar nova despesa? [S/N]: \n").lower().strip()
                if escolha=='n' or escolha=='s':
                    break
                print(f"⚠️ Escolha S ou N")
            if escolha=='n':
                break
        except ValueError:
            erro_input()

#Função para listar gastos fixos e valor total dos gastos
def lista_despesas_fixas_completo(info):
    total=0
    if not info['despesas_fixas']:
        print(f'⚠️ Nenhum gasto fixo cadastrado')
        sleep(0.2)
    else:
        print(f"{AZUL}{'-'*45}{RESET}")
        print(f"{AZUL}{'GASTOS FIXOS':^45}{RESET}")
        print(f"{AZUL}{'-'*45}{RESET}\n")
        for i, d in enumerate(sorted(info['despesas_fixas'],key=lambda d:d['descricao']), start=1):
            print(f"{AZUL}{i:<1}.{RESET}{d['descricao']:<7} {AZUL}-{RESET} R${d['valor']:<3.2f}")
            total+=d['valor']
        print(f'\n{LARANJA}Gasto fixo total:{RESET} R${total:.2f}\n')


#Função para validação de data
def recebe_data(mensagem):
    while True:
        try:
            data_compra=input(mensagem).strip()
            if not data_compra:
                print(f'⚠️ Dado obrigatório')
                sleep(0.2)
                continue
            dia,mes,ano=data_compra.split("/")
            dia=int(dia)
            mes=int(mes)
            ano=int(ano)
            if ano < 100:
                ano+=2000
            data_compra=date(ano,mes,dia)
            return data_compra
        except ValueError:
            erro_input()
        
#Função para entrada de valores
def registra_entrada_valores(info):
    while True:
        try:
            descricao=input(f"Descrição: ").capitalize().strip()
            if not descricao:
                print(f"⚠️ Dado obrigatório")
                sleep(0.2)
                continue
            data=recebe_data(f"Informe a data da entrada [DD/MM/AAAA]: ")
            valor_entrada=float(input(f"Valor: R$"))
            if valor_entrada <=0:
                print(f"❌ Valor inválido")
                sleep(0.2)
                continue
            else:
                registra_transacao(
                    info,
                    descricao=descricao,
                    valor=valor_entrada,
                    tipo='entrada',
                    data=data)
                print(f"✅ Entrada de valor registrada com sucesso!")
                sleep(0.5)
                break
        except ValueError:
            erro_input()

#função de categorias pré-definidas de saída de valores
def lista_categorias_definidas():
    categorias=['Moradia', 'Alimentação', 'Transporte', 'Lazer', 'Saúde', 'Outros']
    for i, categoria in enumerate(categorias,1):
            print(f"{AZUL}{i}.{RESET} {categoria}")
    return categorias

#Função de categorias de despesas
def escolhe_categoria():
    categorias=lista_categorias_definidas()
    while True:
        try:
            escolha=int(input(f"\nEscolha uma categoria: "))
            if 1<= escolha <=len(categorias):
                return categorias[escolha-1]
            else: 
                erro_opcao()
                sleep(0.2)
        except ValueError:
            erro_input()

#Função para cadastro do cartão, com nome, dia de fechamento e dia de vencimento
def cadastra_cartao(info):
    while True:
        nome=input(f"informe o banco ou nome do cartão: ").capitalize().strip()
        if not nome:
            print(f"⚠️ Campo obrigatório!")
            sleep(0.2)
            continue
        if any(cartao['nome']==nome for cartao in info['cartoes']):
            print(f"⚠️ Cartão já cadastrado")
            sleep(0.2)
            continue
        else:
            break
    while True:
        try:
            dia_fechamento=int(input(f"Informe o dia de fechamento do cartão: "))
            if dia_fechamento<1 or dia_fechamento>31:
                print(f"❌ Data inválida")
                sleep(0.2)
            else:
                break
        except ValueError:
            erro_input()
    while True:
        try:
            dia_vencimento=int(input(f"Informe o dia de vencimento do cartão: "))
            if dia_vencimento<1 or dia_vencimento>31:
                print(f"❌ Data inválida")
                sleep(0.2)
            elif dia_vencimento==dia_fechamento:
                print(f"⚠️ A dia de vencimento precisa ser diferente da data de fechamento do cartão")
                sleep(0.2)
            else:
                break
        except ValueError:
            erro_input()
    cartao={
        'nome':nome,
        'fechamento':dia_fechamento,
        'vencimento':dia_vencimento,
        'faturas':{}
    }
    info['cartoes'].append(cartao)
    return cartao

def lista_cartoes_cadastrados(info):
    if not info['cartoes']:
        print(f"⚠️ Nenhum cartão cadastrado")
        return None
    print(f"💳 Cartões cadastrados: ")
    for i, cartao in enumerate(info['cartoes'],1):    
        print(f"{i}. {cartao['nome']}")

#Função para escolha do cartão a ser utilizado no registro da compra
def escolhe_cartao(info):
    lista_cartoes_cadastrados(info)
    while True:
        try:
            escolha=int(input(f"Escolha o cartão desejado: "))
            escolha-=1
            if escolha<0 or escolha >=len(info['cartoes']):
                erro_opcao()
                sleep(0.2)
                continue
            cartao_escolhido=info['cartoes'][escolha]                
            return cartao_escolhido
        except ValueError:
            erro_input()

def coleta_dados_compra():
    descricao=input(f"Descrição: ").capitalize().strip()
    valor_total=float(input(f"Valor total da compra: R$"))
    quantidade_parcelas=int(input(f"Total de parcelas: "))
    categoria=escolhe_categoria()
    data_compra=recebe_data(f"Data da compra [DD/MM/AAAA]: ")

    return descricao, valor_total, quantidade_parcelas, categoria, data_compra

def calcula_fatura_base(data_compra, fechamento):
        if data_compra.day<fechamento:
            return data_compra.month, data_compra.year
        else:
            if data_compra.month==12:
                return 1, data_compra.year+1
            else:
                return data_compra.month+1, data_compra.year
            

def gera_parcelas(valor_total, quantidade_parcelas):
    valor_parcela=round(valor_total/quantidade_parcelas,2)
    parcelas=[valor_parcela] * quantidade_parcelas
    soma=round(sum(parcelas),2)
    diferenca=round(valor_total - soma,2)
    parcelas[-1]= round(parcelas[-1]+diferenca,2)
    return parcelas


def registra_parcelas(info, cartao, descricao, parcelas, categoria, data_compra, mes_base, ano_base, valor_total):
    for i, valor_parcela in enumerate(parcelas):
        mes=mes_base+i
        ano=ano_base
        while mes > 12:
            mes-=12
            ano+=1       
        chave_fatura=f"{mes:02d}/{ano}"
        if chave_fatura not in cartao['faturas']:
            cartao['faturas'][chave_fatura]=[]
        cartao['faturas'][chave_fatura].append({
                'descricao': descricao,
                'valor': -valor_parcela,
                'categoria': categoria,
                'parcela':i+1,
                'total_parcelas': len(parcelas),
                'data_compra':data_compra
            })
        registra_transacao(
            info,
            descricao=descricao,
            tipo='saida',
            valor_total=valor_total,
            valor=-valor_parcela,
            parcela=i+1,
            total_parcelas=len(parcelas),
            categoria=categoria,
            forma_pagamento='cartao_credito',
            cartao=cartao['nome'],
            mes_fatura=chave_fatura,
            data=data_compra
        )


#Função para recolher informações de compras realizadas no cartão de crédito 
def registra_saida_cartao(info,cartao):
    try:
        descricao, valor_total, quantidade_parcelas, categoria, data_compra = coleta_dados_compra()
        if quantidade_parcelas < 1:
            print(f"❌ Quantidade inválida")
            return
        if valor_total <=0:
            print(f"❌ Valor inválido")
            return
        mes_base, ano_base= calcula_fatura_base(data_compra, cartao['fechamento'])
        parcelas= gera_parcelas(valor_total, quantidade_parcelas)
        registra_parcelas(info, cartao, descricao, parcelas, categoria, data_compra, mes_base, ano_base, valor_total)
        print(f"✅ Compra no valor de R${valor_total:.2f} registrada com sucesso em {quantidade_parcelas} parcela(s)")      
        sleep(0.5)              
    except ValueError:
        erro_input()

#Função para saída de valores via débito ou pix
def registra_saida_debito_pix(info):
    while True:
        try:
            descricao=input(f"Descrição: ").capitalize().strip()
            if not descricao:
                print(f"⚠️ Dado obrigatório")
                sleep(0.2)
                continue
            valor_compra=float(input(f"Valor da compra: R$ "))
            if valor_compra < 1:
                print(f"❌ Valor inválido!")
                sleep(0.2)
                continue
            categoria=escolhe_categoria()
            data_compra=recebe_data(f"Data da compra [DD/MM/AAAA]: ")
            registra_transacao(
                info,
                descricao=descricao,
                valor=-valor_compra,
                categoria=categoria,
                tipo='saida',
                forma_pagamento= 'deb_pix',
                data=data_compra
            )
            print(f"✅ Compra registrada com sucesso!")
            sleep(0.2)
            break
        except ValueError:
            erro_input()

#Função para registro de transações, importante para visualização detalhada e filtro em relatórios
def registra_transacao(info, descricao, valor, tipo,valor_total=None, forma_pagamento=None,categoria=None,data=None,cartao=None,mes_fatura=None,parcela=None,total_parcelas=None):
    transacao = {
        'descricao': descricao,
        'valor_total': valor_total,
        'valor':valor,
        'tipo': tipo,
        'forma_pagamento': forma_pagamento,
        'categoria': categoria,
        'data': data,
        'cartao': cartao,
        'mes_fatura': mes_fatura,
        'parcela': parcela,
        'total_parcelas': total_parcelas
    }
    info['transacoes'].append(transacao)
    info['saldo'] += valor
    alerta_saldo(info)

def registra_saida(info):
    while True:
        try:            
            forma_pagamento=int(input(f"Forma de pagamento: "
                        "\n1. Crédito"
                        "\n2. Débito/Pix"
                        "\n>> "))
            sleep(0.2)
            if forma_pagamento==1:
                cartao_escolhido=escolhe_cartao(info)
                registra_saida_cartao(info,cartao_escolhido)
                break
            elif forma_pagamento==2:
                registra_saida_debito_pix(info)
                break
            else:
                erro_opcao()
        except ValueError: 
            erro_input()

#função para exibição do extrato geral, em ordem de data           
def extrato_geral(transacoes, saldo):
    print(f"⏳{CINZA} Carregando extrato...{RESET}\n")
    sleep(1)
    print(f"{AZUL}{'-'*45}{RESET}")
    print(f"{NEGRITO}{'EXTRATO':^45}{RESET}")
    print(f"{AZUL}{'-'*45}{RESET}")
    transacoes_ordenadas=sorted(transacoes, key=lambda t:t['data'] or date.min)    
    for t in transacoes_ordenadas:
        data= t['data']
        if data:
            data_formatada= f"{data.day:02d}/{data.month:02d}/{data.year}"
        else:
            data_formatada='sem data'
        if t['valor']<0:
            valor_formatado=f"{VERMELHO}{t['valor']:+10.2f}{RESET}"
        else:
            valor_formatado=f"{VERDE}{t['valor']:10.2f}{RESET}"
        print(f"{data_formatada:<12} {AZUL}|{RESET} {t['descricao']:<15}{AZUL}|{RESET} {valor_formatado}")
    sleep(1)    
    print(f"\n💰{NEGRITO} SALDO ATUAL:{RESET} R${saldo:.2f}\n")
    

#Função para exibição de extrato com filtro por categoria, em ordem de data
def filtra_por_categoria(transacoes, saldo):
    lista_filtrada=[]
    print(f"{AZUL}Lista de categorias{RESET}")
    sleep(0.5)
    categorias=lista_categorias_definidas()
    try:
        escolha=int(input(f"\nInforme a categoria: "))
        sleep(1)
        if 1<= escolha <= len(categorias):
            categoria_escolhida=categorias[escolha-1]
        else:
            erro_opcao()
            return
    except ValueError:
        erro_input()
    for t in transacoes:          
        if t['categoria'] == categoria_escolhida:
            lista_filtrada.append(t)
    if not lista_filtrada:
        sleep(0.2)
        print(f"\n⚠️ Nenhuma transação encontrada para essa categoria\n")
        sleep(0.2)
    else:
        saida=0
        for l in lista_filtrada:
            if l['valor']<0:
                saida+=l['valor']
        print(f"\n--- CATEGORIA: {categoria_escolhida} --- \n{LARANJA}💸TOTAL DE SAÍDA:{RESET} R${abs(saida):.2f}\n")
        sleep(0.2)
        extrato_geral(lista_filtrada,saldo)
        sleep(0.2)
            

#Função para exibição de extrato com filtro por período, em ordem de data
def filtra_por_periodo(transacoes, saldo):
    while True:
        data_inicial=recebe_data(f'Data inicial [DD/MM/AAAA]: ')
        data_final=recebe_data(f'Data final [DD/MM/AAAA]: ')
        if data_inicial > data_final:
            print(f"\n⚠️ Período inválido, a data inicial deve ser menor que a data final...\n")
            sleep(0.2)
            continue        
        lista_filtrada=[]
        sleep(1)
        for t in transacoes:
            if t['data'] and data_inicial <= t['data'] <= data_final:
                lista_filtrada.append(t)
        if not lista_filtrada:     
            print(f"\n⚠️ Nenhuma transação encontrada para o período fornecido\n")     
            sleep(0.2)            
        else:
            entrada=0
            saida=0
            for l in lista_filtrada:
                if l['valor'] > 0:
                    entrada+=l['valor']
                elif l['valor'] < 0:
                    saida+=l['valor']
            saldo_periodo=entrada+saida

            print(f"\n{MAGENTA}📅 PERÍODO:{RESET} {data_inicial.day:02d}/{data_inicial.month:02d}/{data_inicial.year} até {data_final.day:02d}/{data_final.month:02d}/{data_final.year}")
            print(f"{VERDE}💵 ENTRADA:{RESET} R${entrada:.2f}")
            print(f"{VERMELHO}💸 SAÍDA:{RESET} R${abs(saida):.2f}")
            print(f"{LARANJA}💰 SALDO POR PERÍODO:{RESET} R${saldo_periodo:.2f}\n") 
            sleep(0.2)            
            extrato_geral(lista_filtrada,saldo_periodo)
            sleep(0.2)
            break


#Função para alertar usuário de saldo abaixo do cadastrado ou saldo
def alerta_saldo(info):
    if info['valor_minimo'] is None:
        valor_minimo=500
    else:
        valor_minimo=info['valor_minimo']
    if info['saldo'] < 0:
        print(f"{VERMELHO}⚠️{NEGRITO} Atenção!{RESET} Seu saldo está negativo: {info['saldo']:.2f}{RESET}\n")    
        sleep(0.2)
    elif  info['saldo'] < valor_minimo :
        print(f"{LARANJA}⚠️{NEGRITO} Atenção!{RESET} Seu saldo atual (R${info['saldo']:.2f}) está abaixo de R${valor_minimo:.2f}{RESET}\n")
        sleep(0.2)

        
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def fluxo_inicial(info):
    cadastra_nome(info)
    cadastra_salario(info)
    cadastra_cartao(info)

def menu():
    print(f"{AZUL}{'-'*45}{RESET}")
    print(f"{'MENU':^45}")
    print(f"{AZUL}{'-'*45}{RESET}")
    print(f"{AZUL}1.{RESET} DESPESA FIXA")
    print(f"{AZUL}2.{RESET} CARTÃO DE CRÉDITO")
    print(f"{AZUL}3.{RESET} REGISTRAR ENTRADA")
    print(f"{AZUL}4.{RESET} REGISTRAR SAÍDA")
    print(f"{AZUL}5.{RESET} EXTRATO")
    print(f"{AZUL}6.{RESET} SAIR")
    print(f"{AZUL}{'-'*45}{RESET}")

def define_saudacao(info):
    agora=datetime.now()
    if agora.hour >=0  and agora.hour < 12:
        print(f"\n🌅  Bom dia! {info['nome']}\n")
    elif agora.hour >= 12 and agora.hour < 18:
        print(f"\n☀️  Boa tarde! {info['nome']}\n")
    else:
        print(f"\n🌙  Boa noite! {info['nome']}\n")
    
def menu_despesa_fixa():
        sleep(0.7)
        print(f"{AZUL}{'-'*45}{RESET}")
        print(f"{AZUL}1.{RESET} Cadastrar despesa fixa")
        print(f"{AZUL}2.{RESET} Listar despesa fixa")
        print(f"{AZUL}{'-'*45}{RESET}")

def menu_cartao_de_credito():
        sleep(0.7)
        print(f"{AZUL}{'-'*45}{RESET}")
        print(f"{AZUL}1.{RESET} Cadastrar novo cartão")
        print(f"{AZUL}2.{RESET} Listar cartões cadastrados")
        print(f"{AZUL}{'-'*45}{RESET}")

def menu_extrato():
        sleep(0.7)
        print(f"{AZUL}{'-'*45}{RESET}")
        print(f"{AZUL}1.{RESET} Extrato por categoria")
        print(f"{AZUL}2.{RESET} Extrato por período")
        print(f"{AZUL}3.{RESET} Extrato geral")
        print(f"{AZUL}4.{RESET} Voltar ao menu principal")
        print(f"{AZUL}{'-'*45}{RESET}")

def main(info):
    print(f"\n{NEGRITO}{'BEM VINDO(A)!':^45}{RESET}")
    print(f"{'Vamos realizar seu cadastro inicial':^45}\n")
    sleep(0.5)
    fluxo_inicial(info)
    sleep(0.5)
    define_saudacao(info)
    sleep(0.5)
    while True:
        try:
            menu()
            opcao=int(input(f"{AZUL}>>>> {RESET}"))
            if opcao==1:
                while True:
                    try:
                        sleep(0.2)
                        menu_despesa_fixa()
                        opcao=int(input(f"{AZUL}>>>> {RESET}"))
                        if opcao==1:
                            sleep(0.2)
                            cadastra_despesas_fixas(info)
                            sleep(0.2)
                            break
                        elif opcao==2:
                            sleep(1)
                            lista_despesas_fixas_completo(info)
                            sleep(0.2)
                            break
                        else:
                            erro_opcao()
                    except ValueError:
                        erro_input()
            elif opcao==2:
                while True:
                    try:
                        sleep(0.2)
                        menu_cartao_de_credito()
                        opcao=int(input(f"{AZUL}>>>> {RESET}"))
                        if opcao==1:
                            sleep(0.2)
                            cadastra_cartao(info)
                            sleep(0.2)
                            break
                        elif opcao==2: 
                            sleep(1)
                            lista_cartoes_cadastrados(info)
                            sleep(0.2)
                            break        
                        else:
                            print(f"❌ Opção inválida\n")                                       
                    except ValueError:
                        erro_input()
            elif opcao==3:
                sleep(0.2)
                registra_entrada_valores(info)
                sleep(0.2)
                continue
            elif opcao==4:
                sleep(0.2)
                registra_saida(info)
                sleep(0.2)
                continue
            elif opcao==5:
                menu_extrato()
                while True:
                    try:
                        opcao=int(input(f"{AZUL}>>>> {RESET}"))
                        if opcao==1:
                            sleep(1)
                            filtra_por_categoria(info['transacoes'], info['saldo'])
                            break
                        elif opcao==2:
                            sleep(1)
                            filtra_por_periodo(info['transacoes'], info['saldo'])
                            sleep(0.2)
                            break
                        elif opcao==3:
                            sleep(1)
                            extrato_geral(info['transacoes'], info['saldo'])
                            sleep(0.2)
                            break
                        elif opcao==4:
                            sleep(1)
                            print(f"\n{CINZA}Voltando ao menu principal...\n{RESET}")
                            sleep(1)
                            break
                        else:
                            erro_opcao()
                    except ValueError:
                        erro_input()
            elif opcao==6:
                sleep(1)
                print(f"\n{CINZA}Saindo...{RESET}\n")
                sleep(1)
                break
        except ValueError:
            erro_input()
    


main(info)



























# # Saldo fictício
saldo_teste = 200.00

# # Lista de transações fictícias
transacoes_teste = [
    {'descricao': 'Salário', 'valor': 2000, 'tipo': 'entrada', 'data': date(2026,3,1), 'forma_pagamento': None, 'categoria': 'Outros'},
    {'descricao': 'Aluguel', 'valor': -800, 'tipo': 'saida', 'data': date(2026,3,2), 'forma_pagamento': 'deb_pix', 'categoria': 'Moradia'},
    {'descricao': 'Supermercado', 'valor': -250, 'tipo': 'saida', 'data': date(2026,3,3), 'forma_pagamento': 'deb_pix', 'categoria': 'Alimentação'},
    {'descricao': 'Cinema', 'valor': -50, 'tipo': 'saida', 'data': date(2026,3,5), 'forma_pagamento': 'deb_pix', 'categoria': 'Lazer'},
    {'descricao': 'Plano de Saúde', 'valor': -200, 'tipo': 'saida', 'data': date(2026,3,6), 'forma_pagamento': 'deb_pix', 'categoria': 'Saúde'}
]

# # Chamada da função para testar
# filtra_por_categoria(transacoes_teste, saldo_teste)
#filtra_por_periodo(transacoes_teste, saldo_teste)
#extrato(transacoes_teste,saldo_teste)



































