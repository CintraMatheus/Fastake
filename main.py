# == CONEXÃO COM BANCO DE DADOS DO MYSQL ==
# == OBS.: CONEXÃO DO BANCO DE DADOS NA NUVEM EM ANDAMENTO... ==
#from funcoes_fastake import login, cadastro, ver_restaurantes, menu_f, creditos_add
import mysql.connector
import time
from random import randint
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake_project',
)
cursor = conexao.cursor()

# == FUNÇÃO PARA ADICIONAR CRÉDITOS ==

def creditos_add():
                while True:
                    consulta_senha = input('Digite sua senha para continuar: ') # == VERIFICAÇÃO A PARTIR DA SENHA DO USUÁRIO ==
                    print('Estamos carregando seu saldo de créditos...')
                    time.sleep(1)

                    consulta_credito = 'SELECT credito FROM cadastros WHERE senha = %s' # == ANÁLISE DO CRÉDITO QUE O USUÁRIO POSSUI NO BANCO DE DADOS ==
                    cursor.execute(consulta_credito, (consulta_senha,))
                    resultado = cursor.fetchone()

                    if resultado:
                        credito_atual = int(resultado[0]) # == IMPRIME O NÚMERO DE CRÉDITOS ==
                        print(f'Você tem {credito_atual} créditos')
                        time.sleep(1)

                        add = input('Você deseja adicionar mais créditos? Digite SIM para adicionar: ')
                        if add.upper() == 'SIM':
                            quantia = int(input('Digite a quantia desejada, em R$: \n'))
                            quantia_nova = credito_atual + quantia
                            while True: # == SIMULAÇÃO DE PAGAMENTO AO ADICIONAR CRÉDITOS ==
                                print('=== FORMAS DE PAGAMENTO ===\n' \
                                ' 1 - PIX\n' \
                                ' 2 - Cartão de crédito\n' \
                                ' 3 - Cartão de débito\n '
                                    )
                                forma_pagamento = input('Qual será a forma de pagamento? Digite entre 1,2 ou 3:  ')
                                if forma_pagamento == '1':
                                    print('Estamos processando sua solicitação de pagamento via PIX')
                                    break
                                elif forma_pagamento == '2':
                                    print('Estamos processando sua solicitação de pagamento via cartão de crédito')
                                    break
                                elif forma_pagamento == '3':
                                    print('Estamos processando sua solicitação de pagamento via cartão de débito')
                                    break
                                else:
                                    print('Escolha uma forma de pagamento válida')

                            time.sleep(1)
                            adicionar_quantia = 'UPDATE cadastros SET credito = %s WHERE senha = %s' # == UPDATE DE CRÉDITOS NO BANCO DE DADOS ==
                            cursor.execute(adicionar_quantia, (quantia_nova, consulta_senha))
                            conexao.commit()
                            print('Processo finalizado com sucesso!')
                            time.sleep(1)
                            break
                        else:
                            print('Você está sendo redirecionado para o menu...')
                            time.sleep(1)
                            break
                    else:
                        print('Senha inválida. Tente novamente.\n')

# == FUNÇÃO CADASTRO ==

def cadastro():
            print('Vamos fazer seu cadastro')
            while True:
                cpf = input('Informe seu CPF: ') 
                if not cpf.isdigit(): # == INFORMAR UM CPF VÁLIDO DE ACORDO COM A QUANTIDADE DE NÚMEROS E SE HÁ APENAS NÚMEROS ==
                    print('Escreva apenas números EX: (01234567891)')
                    continue
                cpf = int(cpf)
                if not len(str(cpf)) == 11:
                    print('Escreva 11 números EX: (01234567891)')
                    continue
                break
            checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR SE O CPF JÁ ESTÁ CADASTRADO ==
            cursor.execute(checagem_cpf, (cpf,))
            resultado = cursor.fetchall()
            if len(resultado) != 0:
                print('Esse CPF já está cadastrado')
                while True:
                    logado2 = input('Digite 1, se você já tem login\nDigite 2 caso tenha digitado errado e queira repetir: ')
                    if not logado2.isdigit(): # == O USUÁRIO ESCOLHE SE QUER RETORNAR AO LOGIN COM ESSE CPF OU REPETIR A DIGITAÇÃO DE CPF ==
                        print('Digite apenas "1" ou "2"')
                        continue
                    logado2 = int(logado2)
                    if not logado2 >= 1 and logado2 <= 2:
                        print('Digite apenas "1" ou "2"')
                        continue
                    if logado2 == 1:
                        login()
                        exit()   # == TENTAR LOGAR NOVAMENTE ==
                        break
                    if logado2 == 2:
                        cadastro()
                        exit()    # == REPETIR O CPF ==
                        break
                    break
            while True:
                senha = input('Qual vai ser sua senha ?\nA senha deve conter exatamente 4 números: ')
                if not senha.isdigit():
                    print('Escreva apenas números, no formato (1234)')
                    continue    # == CRIAÇÃO DE SENHA ATRAVÉS DOS FORMATOS VÁLIDOS ( APENAS NÚMEROS E 4 DÍGITOS ) ==
                if not len(str(senha)) == 4:
                    print('Escreva exatamente 4 números, no formato (1234)')
                    continue
                break
            codigo = randint(999, 10000) # == GERAÇÃO DE UM CÓDIGO PESSOAL ALEATÓRIO PARA RECUPERAÇÃO DE SENHA E OUTROS SERVIÇOS ==
            adicionar = f'INSERT INTO cadastros (cpf, senha, codigo) VALUE (%s, %s, %s)' # == CREATE DE INFORMAÇÕES NO BANCO DE DADOS ==
            cursor.execute(adicionar, (cpf, senha, codigo))
            conexao.commit()
            print(f'\033[31mFOI CRIADO UM CÓDIGO PESSOAL PARA VOCÊ USAR EM CASO DE RECUPERAÇÃO DE SENHA, NÃO O PERCA!\nSEU CÓDIGO É {codigo}\033[0m')
            print('Você foi cadastrado com sucesso!\nAgora você retornará ao login, e escreva seus dados cadastrados')
            login() # == IDA AO LOGIN PARA ENTRAR NA SUA CONTA ==
            exit()

                        

# == FUNÇÃO VER RESTAURANTES ==
def ver_restaurantes():
                print('Estamos lhe redirecionando para a página de restaurantes participantes!')
                time.sleep(1)
                opcoes = 'SELECT restaurante FROM restaurantes' # == LEITURA ( READ ) DOS RESTAURANTES CADASTRADOS NO BANCO DE DADOS ==
                cursor.execute(opcoes)
                resultado = cursor.fetchall()
                while True:
                    for i, row in enumerate(resultado, start=1):
                        print(f'Restaurante {i} : {row[0]}') # == IMPRESSÃO DOS RESTAURANTES PARTICIPANTES ==
                    escolha = input('Escolha entre as três opções disponíveis:\nDigite 1,2 ou 3: ')
                    if escolha == '1': # == PIZZARIA ==
                        cursor.execute("SELECT prato_principal FROM restaurantes WHERE restaurante = 'Pizzaria'") # == LEITURA DO PRATO ==
                        prato_pizzaria = cursor.fetchone()
                        prato_pizzaria = prato_pizzaria[0]
                        print(f'Bem-vindo à Pizzaria!\n\nEsse é o prato principal : {prato_pizzaria}\n')
                        decisao = input('Digite SIM caso queira realizar o pedido ou NAO para retornar ao menu: ') 
                        while True:
                            if decisao.upper() == 'SIM':
                                cursor.execute("SELECT Valor FROM restaurantes WHERE restaurante = 'Pizzaria'") # == LEITURA DO VALOR ==
                                valor_pizza = cursor.fetchone()
                                time.sleep(1)
                                print(f'O valor do seu pedido é de\nR${valor_pizza[0]}')
                                confirmar_compra = input('Digite sua senha para confirmar a compra: ') # == VERIFICAÇÃO FINAL DE COMPRA ATRAVÉS DA SENHA ==
                                verificacao_senha = ('SELECT * FROM cadastros WHERE senha = %s')
                                cursor.execute(verificacao_senha, (confirmar_compra,))
                                resultado_senha = cursor.fetchall()
                            elif decisao.upper() == 'NAO':
                                print('Você está sendo redirecionado para o menu!')
                                time.sleep(1)
                                menu_f()
                                break
                            else:
                                print('Tente uma opção válida!')
                                time.sleep(1)
                                
                            
                            if resultado_senha:
                                consulta_credito = 'SELECT credito FROM cadastros WHERE senha = %s'
                                cursor.execute(consulta_credito, (confirmar_compra,))
                                resultado = cursor.fetchone()
                                credito = int(resultado[0])
                                if credito >= 45: # == VERIFICAR SE O USUÁRIO POSSUI CRÉDITOS SUFICIENTES ATRAVÉS DE UMA CONSULTA AO BANCO DE DADOS ==
                                    print('Estamos processando-o...')
                                    time.sleep(1)
                                    credito_desconto = credito - 45
                                    cursor.execute('UPDATE cadastros SET credito = %s WHERE senha = %s', (credito_desconto, confirmar_compra)) # == UPDATE DOS CRÉDITOS SUBTRAIDOS PELO VALOR DO PRATO ==
                                    conexao.commit()
                                    cursor.execute('SELECT ticketpizzaria FROM cadastros WHERE senha = %s', (confirmar_compra, )) # TESTE PARA GERAR TICKETS !!!
                                    resultado_qtdatual = cursor.fetchone()
                                    resultado_format = int(resultado_qtdatual[0])
                                    qtd_ticket_atual = (resultado_format) + 1
                                    cursor.execute('UPDATE cadastros SET ticketpizzaria = %s WHERE senha = %s', (qtd_ticket_atual, confirmar_compra))
                                    conexao.commit()
                                    print('Compra realizada com sucesso e Ticket gerado\nEstamos lhe redirecionando para o menu..')
                                    time.sleep(1)
                                    
                                    break
                                else:
                                    add_credito = True
                                    while add_credito: # == PERGUNTAR AO USUÁRIO SE ELE QUER ADICIONAR CRÉDITOS OU RETORNAR AO MENU ==
                                        decisao_credito = input('Você não tem créditos para realizar essa compra!\nDigite 1 para adicionar créditos ou 2 para retornar ao menu: ')
                                        if decisao_credito == '1':
                                            creditos_add()
                                            ver_restaurantes()
                                        elif decisao_credito == '2':
                                            print('Você está sendo redirecionado para o menu...')
                                            time.sleep(1)
                                            
                                            menu_f()
                                        else:
                                            print('Tente uma opção válida!')
                            else:
                                print('Senha não válida, tente novamente')
                                
                    elif escolha == '2': # == HAMBURGUERIA ==
                        cursor.execute("SELECT prato_principal FROM restaurantes WHERE restaurante = 'Hamburgueria'") # == LEITURA DO PRATO ==
                        prato_hamburgueria = cursor.fetchone() 
                        print(f'Bem-vindo à Hamburgueria!\n\nEsse é o prato principal : {prato_hamburgueria[0]}\n')
                        decisao = input('Digite SIM caso queira realizar o pedido ou NAO para retornar ao menu: ')
                        while True:
                            if decisao.upper() == 'SIM':
                                cursor.execute("SELECT Valor FROM restaurantes WHERE restaurante = 'Hamburgueria'") # == LEITURA DO VALOR ==
                                valor_hamburguer = cursor.fetchone()
                                time.sleep(1)
                                print(f'O valor do seu pedido é de\nR${valor_hamburguer[0]}')
                                confirmar_compra = input('Digite sua senha para confirmar a compra: ') # == VERIFICAÇÃO DE SENHA ==
                                verificacao_senha = ('SELECT * FROM cadastros WHERE senha = %s')
                                cursor.execute(verificacao_senha, (confirmar_compra,))
                                resultado_senha = cursor.fetchall()
                            elif decisao.upper() == 'NAO':
                                print('Você está sendo redirecionado para o menu!')
                                time.sleep(1)
                                menu_f()
                                break
                            else:
                                print('Tente uma opção válida!')
                                time.sleep(1)
                            
                            if resultado_senha:
                                consulta_credito = 'SELECT credito FROM cadastros WHERE senha = %s'
                                cursor.execute(consulta_credito, (confirmar_compra,))
                                resultado = cursor.fetchone()
                                credito = int(resultado[0])
                                if credito >= 40: # == ANÁLISE PARA VER SE O USUÁRIO POSSUI CRÉDITO ==
                                    print('Estamos processando-o...')
                                    time.sleep(1)
                                    credito_desconto = credito - 40 
                                    cursor.execute('UPDATE cadastros SET credito = %s WHERE senha = %s', (credito_desconto, confirmar_compra))
                                    conexao.commit() # == SUBTRAÇÃO DE CRÉDITOS DO USUÁRIO DE ACORDO COM O VALOR DO PEDIDO ==
                                    cursor.execute('SELECT tickethamburgueria FROM cadastros WHERE senha = %s', (confirmar_compra, )) # TESTE PARA GERAR TICKETS !!!
                                    resultado_qtdatual = cursor.fetchone()
                                    resultado_format = int(resultado_qtdatual[0])
                                    qtd_ticket_atual = (resultado_format) + 1
                                    cursor.execute('UPDATE cadastros SET tickethamburgueria = %s WHERE senha = %s', (qtd_ticket_atual, confirmar_compra))
                                    conexao.commit()
                                    print('Compra realizada com sucesso e Ticket gerado\nEstamos lhe redirecionando para o menu..')
                                    time.sleep(1)
                                    
                                    break
                                else:
                                    add_credito = True
                                    while add_credito:
                                        decisao_credito = input('Você não tem créditos para realizar essa compra!\nDigite 1 para adicionar créditos ou 2 para retornar ao menu: ')
                                        if decisao_credito == '1':
                                            creditos_add() 
                                            ver_restaurantes()
                                        elif decisao_credito == '2':
                                            print('Você está sendo redirecionado para o menu...')
                                            time.sleep(1)
                                            
                                            menu_f()
                                        else:
                                            print('Tente uma opção válida!')
                            else:
                                print('Senha não válida, tente novamente')

                    elif escolha == '3': # == COMIDA BR ==
                        cursor.execute("SELECT prato_principal FROM restaurantes WHERE restaurante = 'Comida Brasileira'") # == LEITURA DE PRATO ==
                        prato_comidabr = cursor.fetchone()
                        print(f'Bem-vindo ao restaurante de comida brasileira!\n\nEsse é o prato principal :{prato_comidabr[0]}\n')
                        decisao = input('Digite SIM caso queira realizar o pedido ou NAO para retornar ao menu: ')
                        while True:
                            if decisao.upper() == 'SIM':
                                cursor.execute("SELECT Valor FROM restaurantes WHERE restaurante = 'Comida Brasileira'")
                                valor_comidabr = cursor.fetchone() # == LEITURA DO VALOR ==
                                time.sleep(1)
                                print(f'O valor do seu pedido é de\nR${valor_comidabr[0]}') 
                                confirmar_compra = input('Digite sua senha para confirmar a compra: ') # == VERIFICAÇÃO PELA SENHA ==
                                verificacao_senha = ('SELECT * FROM cadastros WHERE senha = %s')
                                cursor.execute(verificacao_senha, (confirmar_compra,))
                                resultado_senha = cursor.fetchall()
                            elif decisao.upper() == 'NAO':
                                print('Você está sendo redirecionado para o menu!')
                                time.sleep(1)
                                menu_f()
                                break
                            else:
                                print('Tente novamente!')
                                time.sleep(1)
                            
                            if resultado_senha:
                                consulta_credito = 'SELECT credito FROM cadastros WHERE senha = %s'
                                cursor.execute(consulta_credito, (confirmar_compra,))
                                resultado = cursor.fetchone()
                                credito = int(resultado[0])
                                if credito >= 35: # == ANÁLISE DA SITUAÇÃO DE CRÉDITOS DO USUÁRIO ==
                                    print('Estamos processando-o...')
                                    time.sleep(1)
                                    credito_desconto = credito - 35 # == UPDATE DOS CRÉDITOS ATUAIS - O VALOR DO PEDIDO ==
                                    cursor.execute('UPDATE cadastros SET credito = %s WHERE senha = %s', (credito_desconto, confirmar_compra))
                                    conexao.commit()
                                    cursor.execute('SELECT ticketcomidabr FROM cadastros WHERE senha = %s', (confirmar_compra, )) # TESTE PARA GERAR TICKETS !!!
                                    resultado_qtdatual = cursor.fetchone()
                                    resultado_format = int(resultado_qtdatual[0])
                                    qtd_ticket_atual = (resultado_format) + 1
                                    cursor.execute('UPDATE cadastros SET ticketcomidabr = %s WHERE senha = %s', (qtd_ticket_atual, confirmar_compra))
                                    conexao.commit()
                                    print('Compra realizada com sucesso e Ticket gerado\nEstamos lhe redirecionando para o menu..')
                                    time.sleep(1)
                                    
                                    break
                                else:
                                    add_credito = True
                                    while add_credito:
                                        decisao_credito = input('Você não tem créditos para realizar essa compra!\nDigite 1 para adicionar créditos ou 2 para retornar ao menu: ')
                                        if decisao_credito == '1':
                                            creditos_add()
                                            ver_restaurantes()
                                        elif decisao_credito == '2':
                                            print('Você está sendo redirecionado para o menu...')
                                            time.sleep(1)
                                            
                                            menu_f()
                                        else:
                                            print('Tente uma opção válida!')
                            else:
                                print('Senha não válida, tente novamente')   
                    else:
                        print('Digite uma opção válida de restaurante')
                    break
                menu_f()

# == MENU INTERATIVO COM 5 OPÇÕES DISPONÍVEIS ==

def menu_f():
    opcoes_menu = (
    '1 - Trocar senha'
    '\n2 - Ver crédito'
    '\n3 - Ver restaurantes'
    '\n4 - Ver tickets'
    '\n5 - Deletar conta'
    '\n6 - Ir para página de login'
    )
    menu = True
    while menu: # == LOOP PARA SEMPRE VOLTAR AO MENU PRINCIPAL AO FINAL DE UM PROCESSO ESPECÍFICO ==
        opcao_menu = input(str(f'Menu:\n{opcoes_menu}\nDigite aqui uma opção válida: '))

        # == TROCAR SENHA ==

        if opcao_menu == '1':
            verificacao_codigo = True
            while verificacao_codigo:
                codigo_trocar = int(input('Digite seu código de segurança: '))
                consulta = 'SELECT * FROM cadastros WHERE codigo = %s'
                cursor.execute(consulta, (codigo_trocar,)) # == VERIFICAÇÃO A PARTIR DO CÓDIGO DE SEGURANÇA DO USUÁRIO ==
                resultado = cursor.fetchone()
                if resultado:
                    print('Seu código foi validado com sucesso!')
                    time.sleep(1)
                    try:
                        nova_senha = (input('Digite aqui sua nova senha (4 dígitos): '))
                        if len(nova_senha) == 4 and nova_senha.isdigit(): # == VERIFICAÇÃO PARA SENHA DE 4 DÍGITOS ==
                            comando_novasenha = f'UPDATE cadastros SET senha = %s WHERE codigo = %s' # == UPDATE DA SENHA NO BANCO DE DADOS ==
                            cursor.execute(comando_novasenha, (nova_senha, codigo_trocar))
                            conexao.commit()
                            time.sleep(1)
                            print('Senha salva com sucesso!\nVocê está sendo redirecionado para o menu')
                            time.sleep(1)
                            verificacao_codigo = False
                            menu = True
                        else:
                            raise ValueError
                    except ValueError: # == ERRO TRATÁVEL PARA SENHA QUE CONTER CARACTERES ( STRINGS ) ==
                            print('Senha inválida!')
                            time.sleep(1)
                            senha_invalida = True
                            while senha_invalida: # == LOOP PARA, ENQUANTO A SENHA NÃO CONTER AS RESTRIÇÕES, SOLICITAR AO USUÁRIO NOVAMENTE A SENHA ==
                                try:
                                    nova_senha = (input('Tente novamente: '))
                                    if len(nova_senha) == 4 and nova_senha.isdigit():
                                        time.sleep(1)
                                        comando_novasenha = f'UPDATE cadastros SET senha = {nova_senha} WHERE codigo = %s' # == UPDATE NO BANCO DE DADOS ==
                                        cursor.execute(comando_novasenha, (codigo_trocar,))
                                        conexao.commit()
                                        print('Senha salva com sucesso!')
                                        time.sleep(1)
                                        print('Você está sendo redirecionado para o menu!')
                                        time.sleep(1)
                                        senha_invalida = False
                                        menu = True
                                        verificacao_codigo = False
                                    else:
                                        print('Senha deve ter 4 dígitos!')
                                        senha_invalida = True
                                except ValueError:
                                    print('Você deve digitar apenas números')
                else:
                    print('Código inválido, tente novamente')
                    time.sleep(1)
            menu_f()
        # == VER CRÉDITO ==
        elif opcao_menu == '2': 
            creditos_add()
            menu_f()
         
        # == VER RESTAURANTES ==

        elif opcao_menu == '3':
            ver_restaurantes()
            

        # == VER TICKET ==
        elif opcao_menu == '4':
            ticket = True
            while ticket:
                senha_verificar = input('Digite aqui sua senha para continuar: ')
                cursor.execute('SELECT * FROM cadastros WHERE senha = %s', (senha_verificar,))
                resultado = cursor.fetchall()
                if resultado:
                    cursor.execute('SELECT ticketpizzaria FROM cadastros WHERE senha = %s', (senha_verificar,))
                    resultado_pizzaria = cursor.fetchall()
                    cursor.execute('SELECT tickethamburgueria FROM cadastros WHERE senha = %s', (senha_verificar,))
                    resultado_hamburgueria = cursor.fetchall()
                    cursor.execute('SELECT ticketcomidabr FROM cadastros WHERE senha = %s', (senha_verificar,))
                    resultado_comida_br = cursor.fetchall()
                    qtd_ticket_pizzaria = int(resultado_pizzaria[0][0])
                    qtd_ticket_hamburgueria = int(resultado_hamburgueria[0][0])
                    qtd_ticket_comida_br = int(resultado_comida_br[0][0])
                    print('Estamos carregando seus tickets...')
                    time.sleep(1)
                    print(f'Você tem:\n{qtd_ticket_pizzaria} tickets na Pizzaria!\n{qtd_ticket_hamburgueria} tickets na Hamburgueria!\n{qtd_ticket_comida_br} tickets na Comida Brasileira!')
                    decisao_ticket = input('Deseja retornar ao menu? Digite 1 para retornar : ')
                    if decisao_ticket == '1':
                        menu_f()
                        break
                    else:
                        print('Estamos lhe redirecionando para o início dessa aba!')
                        time.sleep(1)
                else:
                    print('Senha inválida, digite novamente')
            menu_f()

        # == DELETAR CONTA ==

        elif opcao_menu == '5':
            cpf = str((input('Digite o CPF da conta a ser apagada: '))) # == VERIFICAÇÃO POR CPF ==
            consulta2 = 'SELECT * FROM cadastros WHERE cpf = %s'
            cursor.execute(consulta2, (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                print('CPF validado!')
                time.sleep(1)
            else:
                while True: # == LOOP PARA SOLICITAR UM CPF VÁLIDO ATÉ O USUÁRIO ACERTAR ==
                    cpf = str((input('Digite novamente um CPF válido!')))
                    consulta3 = 'SELECT * FROM cadastros WHERE cpf = %s'
                    cursor.execute(consulta3, (cpf,))
                    resultado = cursor.fetchone()
                    if resultado:
                        print('CPF validado!')
                        time.sleep(1)
                        False
                    else:
                        print('Escreva seu CPF correto: ')
                        time.sleep(1) 
                        continue  
            decisao_delete = str(input('Digite SIM para confirmar a exclusão da conta: ')) # == CONFIRMAÇÃO DE EXCLUSÃO ==
            decisao_invalida = True
            if decisao_delete.upper() == 'SIM':
                comando = 'DELETE FROM cadastros WHERE cpf = %s ' # == DELETE DA CONTA NO BANCO DE DADOS ==
                cursor.execute(comando, (cpf,))
                conexao.commit()
                print('Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial')
                time.sleep(1)
            else:
                while decisao_invalida:
                    decisao_delete2 = str(input('Digite SIM para confirmar a exclusão da conta ou NAO para retornar ao menu! '))
                    if decisao_delete2.upper() == 'SIM':
                        comando = 'DELETE FROM cadastros WHERE cpf = %s'
                        cursor.execute(comando, (cpf,)) # == DELETE DA CONTA NO BANCO DE DADOS ==
                        conexao.commit()
                        print('Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial ')
                        time.sleep(1)
                        break
                    elif decisao_delete2.upper() == 'NAO':
                        menu_f()
                        time.sleep(1)
                        break
                    else:
                        print('Tente novamente uma opção válida!')
                        time.sleep(1)
            inicio()
        elif opcao_menu == '6':
            login()
        else:
            print('Tente uma opção válida!')
            time.sleep(1)

#MENU!!!

def login():
    #retorna ao login quando quiser
    while True:
        cpf = (input('Qual é o seu CPF (digite apenas os números): '))
        if not cpf.isdigit():
            print('Digite apenas números, no formato (12345678912)') # == VERIFICAR SE HÁ APENAS NÚMEROS ==
            continue
        cpf = int(cpf)
        if not len(str(cpf)) == 11: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DO CPF ==
            print('Digite exatamente 11 números')
            continue
        break
    while True:
        senha = (input('Qual é sua senha ? '))
        if not senha.isdigit(): # == VERIFICAÇÃO SE HÁ APENAS NÚMEROS ==
            print('Escreva apenas números EX: (1234)')
            continue
        senha = senha
        if not len(str(senha)) == 4: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DA SENHA ==
            print('Escreva exatamente 4 digitos EX: (1234)')
            continue
        checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR EXISTÊNCIA DO CPF NO BANCO DE DADOS ==
        cursor.execute(checagem_cpf, (cpf,))
        resultado = cursor.fetchall()
        if len(resultado) != 0: 
            checagem_senha = "SELECT * FROM cadastros WHERE cpf = %s AND senha = %s"
            cursor.execute(checagem_senha, (cpf, senha))
            resultado = cursor.fetchone() # == LEITURA DO CPF E SENHA NO BANCO DE DADOS ==
            if not resultado:
                while True: # == OPÇÃO DE TENTAR NOVAMENTE DIGITAR A SENHA OU RECUPERAR A SENHA ESQUECIDA ==
                    decisao_senha = input('Sua senha está errada, deseja tentar novamente ?\nSe desejar tentar novamente digite 1, se desejar recuperar senha digite 2:  ')
                    if not decisao_senha.isdigit(): # == VERIFICAÇÃO DE OPÇÃO VÁLIDA ==
                        print('digite apenas 1 ou 2')
                        continue
                    decisao_senha = int(decisao_senha)
                    if not 2 >= decisao_senha or decisao_senha >= 1:
                        print('Digite apenas 1 ou 2')
                    if decisao_senha == 1:
                        break
                    if decisao_senha == 2:
                        print('Você será redirecionado para recuperar a sua senha')
                        while True: # == RECUPERAÇÃO DE SENHA ATRAVÉS DO CÓDIGO PESSOAL ==
                            codigo = input('Informe seu código pessoal para recuperar sua senha: ')
                            if not codigo.isdigit(): # == VERIFICAÇÃO SE HÁ APENAS NÚMEROS ==
                                print('Digite apenas números, com 5 digitos EX: (12345)')
                                continue
                            codigo = int(codigo)
                            if not len(str(codigo)) == 5: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS ==
                                print('Digite apenas números, com 5 digitos EX: (12345)')
                            checagem_codigo = "SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s"
                            cursor.execute(checagem_codigo, (cpf, codigo))
                            resultado = cursor.fetchone()
                            if not resultado:
                                print('Seu código está incorreto, tente novamente')
                                continue
                            senha = randint (1000, 10000) # == GERAÇÃO DE SENHA ALEATÓRIA PARA O USUÁRIO APÓS VALIDAÇÃO DE CÓDIGO ==
                            atualizar = "UPDATE cadastros SET senha = %s WHERE cpf = %s" # == UPDATE NO BANCO DE DADOS ==
                            cursor.execute(atualizar, (senha, cpf))
                            conexao.commit()
                            print(f'Agora sua nova senha é {senha}\nGuarde sua senha\nAgora você será direcionado ao login')
                            login()
                            break
                        exit()
                continue
            else:
                print('Você fez o login com sucesso')
                menu_f() # == IDA AO MENU ==
                exit()
        else:
            print('Seu CPF está errado')
            while True: # == OPÇÃO AO USUÁRIO DE TENTAR NOVAMENTE DIGITAR O CPF OU CADASTRAR UMA NOVA CONTA ==
                logado = input('Se você tiver apenas digitado seu CPF errado: digite 1\nSe você não tiver conta, para ser redirecionado ao cadastro: digite 2\nO que você deseja ?: ')
                if not logado.isdigit():
                    print('Digite apenas 1 ou 2')
                    continue                           # == VERIFICAÇÃO DE OPÇÃO VÁLIDA ==
                logado = int(logado)
                if not logado >= 1 and logado <= 2:
                    print('Digite apenas 1 ou 2')
                    continue
                break
            if logado == 1:
                print('Você será redirecionado para o login novamente')
                login() # == TENTAR LOGAR NOVAMENTE ==
                exit()
            if logado == 2:
                def cadastro():
                    print('Vamos fazer seu cadastro')
                    while True:
                        cpf = input('Informe seu CPF: ') 
                        if not cpf.isdigit(): # == INFORMAR UM CPF VÁLIDO DE ACORDO COM A QUANTIDADE DE NÚMEROS E SE HÁ APENAS NÚMEROS ==
                            print('Escreva apenas números EX: (01234567891)')
                            continue
                        cpf = int(cpf)
                        if not len(str(cpf)) == 11:
                            print('Escreva 11 números EX: (01234567891)')
                            continue
                        break
                    checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR SE O CPF JÁ ESTÁ CADASTRADO ==
                    cursor.execute(checagem_cpf, (cpf,))
                    resultado = cursor.fetchall()
                    if len(resultado) != 0:
                        print('Esse CPF já está cadastrado')
                        while True:
                            logado2 = input('Digite 1, se você já tem login\nDigite 2 caso tenha digitado errado e queira repetir: ')
                            if not logado2.isdigit(): # == O USUÁRIO ESCOLHE SE QUER RETORNAR AO LOGIN COM ESSE CPF OU REPETIR A DIGITAÇÃO DE CPF ==
                                print('Digite apenas "1" ou "2"')
                                continue
                            logado2 = int(logado2)
                            if not logado2 >= 1 and logado2 <= 2:
                                print('Digite apenas "1" ou "2"')
                                continue
                            if logado2 == 1:
                                login()
                                exit()   # == TENTAR LOGAR NOVAMENTE ==
                                break
                            if logado2 == 2:
                                cadastro()
                                exit()    # == REPETIR O CPF ==
                                break
                            break
                    while True:
                        senha = str(input('Qual vai ser sua senha ?\nA senha deve conter exatamente 4 números: '))
                        if not senha.isdigit():
                            print('Escreva apenas números, no formato (1234)')
                            continue    # == CRIAÇÃO DE SENHA ATRAVÉS DOS FORMATOS VÁLIDOS ( APENAS NÚMEROS E 4 DÍGITOS ) ==
                        if not len(str(senha)) == 4:
                            print('Escreva exatamente 4 números, no formato (1234)')
                            continue
                        break
                    cpf = str(cpf)
                    senha = str(senha)
                    codigo = randint(999, 10000) # == GERAÇÃO DE UM CÓDIGO PESSOAL ALEATÓRIO PARA RECUPERAÇÃO DE SENHA E OUTROS SERVIÇOS ==
                    adicionar = f'INSERT INTO cadastros (cpf, senha, codigo) VALUES (%s, %s, %s)' # == CREATE DE INFORMAÇÕES NO BANCO DE DADOS ==
                    cursor.execute(adicionar, (cpf, senha, codigo))
                    conexao.commit()
                    print(f'\033[31mFOI CRIADO UM CÓDIGO PESSOAL PARA VOCÊ USAR EM CASO DE RECUPERAÇÃO DE SENHA, NÃO O PERCA!\nSEU CÓDIGO É {codigo}\033[0m')
                    print('Você foi cadastrado com sucesso!\nAgora você retornará ao login, e escreva seus dados cadastrados')
                    login() # == IDA AO LOGIN PARA ENTRAR NA SUA CONTA ==
                    exit()
                cadastro()

# == INICIO DO PROGRAMA ==
def inicio():
    iniciar = True
    while iniciar:
        inicio = input('Bem vindo à Fastake!!\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
        if inicio == '1':
            print('Você está sendo redirecionado para o cadastro!')
            time.sleep(1)
            cadastro()
            break
        elif inicio == '2':
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            login()
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue
inicio()