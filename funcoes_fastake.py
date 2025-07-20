import mysql.connector
import time
from random import randint
from unidecode import unidecode
from email_validator import EmailNotValidError, validate_email
import funções_ADM as fa

# Remove the global conexao and cursor from here in funcoes_fastake.py
# as they will be passed into the functions.

# == INICIO DO PROGRAMA ==
def inicio(conexao, cursor):
    while True:
        escolha = input("Bem vindo à Fastake!\n" \
        "Se deseja ir para a parte de adiministradores: digite 1\n" \
        "Se deseja ir para a parte de usuários: digite 2\n")
        if escolha == '1':
            print('Você está sendo redirecionado para a página de administrador!')
            time.sleep(1)
            adm(conexao, cursor) # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para a página de usuário!')
            time.sleep(1)
            user(conexao, cursor) # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue

def adm(conexao, cursor):
    while True:
        escolha = input('Bem vindo administrador!\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
        if escolha == '1':
            print('Você está sendo redirecionado para o cadastro!')
            time.sleep(1)
            fa.Adm.cadastro_adm(conexao, cursor) # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            fa.Adm.login_adm(conexao, cursor) # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue

def user(conexao, cursor): # Add cursor as an argument
    user = True
    while user:
        escolha = input('Bem vindo usuário!\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
        if escolha == '1':
            print('Você está sendo redirecionado para o cadastro!')
            time.sleep(1)
            cadastro(conexao, cursor) # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            login(conexao, cursor) # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue

# == MENU INTERATIVO ==

def menu_f(conexao, cursor): # Add conexao and cursor as arguments
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
            def trocar_senha(conexao, cursor): # Add conexao and cursor as arguments

                verificacao_codigo = True
                while verificacao_codigo:
                    try: # Added try-except for integer input
                        codigo_trocar = int(input('Digite seu código de segurança: '))
                    except ValueError:
                        print("Por favor, digite apenas números para o código de segurança.")
                        time.sleep(1)
                        continue
                    consulta = 'SELECT * FROM cadastros WHERE codigo = %s'
                    cursor.execute(consulta, (codigo_trocar,)) # == VERIFICAÇÃO A PARTIR DO CÓDIGO DE SEGURANÇA DO USUÁRIO ==
                    resultado = cursor.fetchone()
                    if resultado:
                        print('Seu código foi validado com sucesso!')
                        time.sleep(1)
                        try:
                            nova_senha = (input('Digite aqui sua nova senha (4 dígitos): '))
                            if len(nova_senha) == 4 and nova_senha.isdigit(): # == VERIFICAÇÃO PARA SENHA DE 4 DÍGITOS ==
                                comando_novasenha = 'UPDATE cadastros SET senha = %s WHERE codigo = %s' # == UPDATE DA SENHA NO BANCO DE DADOS ==
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
                                            # Use parameterized query instead of f-string for security and correctness
                                            comando_novasenha = 'UPDATE cadastros SET senha = %s WHERE codigo = %s'
                                            cursor.execute(comando_novasenha, (nova_senha, codigo_trocar))
                                            conexao.commit()
                                            print('Senha salva com sucesso!')
                                            time.sleep(1)
                                            print('Você está sendo redirecionado para o menu!')
                                            time.sleep(1)
                                            senha_invalida = False
                                            menu = True
                                            verificacao_codigo = False
                                        else:
                                            print('Senha deve ter 4 dígitos e conter apenas números!') # Clarified message
                                            senha_invalida = True
                                    except ValueError:
                                        print('Você deve digitar apenas números')
                    else:
                        print('Código inválido, tente novamente')
                        time.sleep(1)
                menu_f(conexao, cursor) # Pass conexao and cursor
            trocar_senha(conexao, cursor) # Pass conexao and cursor
        # == VER CRÉDITO ==
        elif opcao_menu == '2':
            def creditos_add(conexao, cursor): # Add conexao and cursor as arguments
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
                            while True: # Added loop for valid integer input
                                try:
                                    quantia = int(input('Digite a quantia desejada, em R$: \n'))
                                    break
                                except ValueError:
                                    print("Por favor, digite apenas números para a quantia.")
                                    time.sleep(1)

                            quantia_nova = credito_atual + quantia
                            while True: # == SIMULAÇÃO DE PAGAMENTO AO ADICIONAR CRÉDITOS ==
                                print('=== FORMAS DE PAGAMENTO ===\n' \
                                ' 1 - PIX\n' \
                                ' 2 - Cartão de crédito\n' \
                                ' 3 - Cartão de débito\n '
                                    )
                                forma_pagamento = input('Qual será a forma de pagamento? Digite entre 1,2 ou 3:  ')
                                if forma_pagamento in ['1', '2', '3']: # Check for valid input
                                    print(f'Estamos processando sua solicitação de pagamento via {"PIX" if forma_pagamento == "1" else "cartão de crédito" if forma_pagamento == "2" else "cartão de débito"}')
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
                        continue
                menu_f(conexao, cursor) # Pass conexao and cursor
            creditos_add(conexao, cursor) # Pass conexao and cursor

        # == VER RESTAURANTES ==

        elif opcao_menu == '3':
            def ver_restaurantes(conexao, cursor, cpf): # Add conexao and cursor as arguments

                print('Estamos lhe redirecionando para a página de restaurantes participantes!')
                time.sleep(1)
                opcoes = 'SELECT id, restaurante FROM restaurantes' # == LEITURA ( READ ) DOS RESTAURANTES CADASTRADOS NO BANCO DE DADOS ==
                cursor.execute(opcoes)
                resultado = cursor.fetchall()
                while True:
                    print('----Restaurantes disponiveis----')
                    for i, lista_restaurantes in enumerate(resultado, start=1):
                        num_restaurante = lista_restaurantes[0]
                        nome_restaurante = lista_restaurantes[1]
                        print(f'Restaurante : {nome_restaurante} - {num_restaurante}') # == IMPRESSÃO DOS RESTAURANTES PARTICIPANTES ==
                    while True:
                        escolha = input('Escolha entre as opções disponíveis (o número ao lado do restaurante): ')
                        if not escolha.isdigit():
                            print('Digite apenas números')
                            continue
                        escolha = int(escolha)
                        if not 1<= escolha <= len(lista_restaurantes):
                            print(f'A opção escolhida não é válida, escolha uma opção entre 1 e {len(lista_restaurantes)}')
                            continue
                        cursor.execute(f"SELECT restaurante FROM restaurantes WHERE id = {escolha}")
                        nome = cursor.fetchone()
                        print(f"Bem vindo(a) ao restaurante {nome}, aqui está o cardápio:")
                        cursor.execute(f"SELECT nome, valor FROM pratos WHERE id_restaurante = {escolha}")
                        pratos = cursor.fetchall()
                        for i, (nome, valor) in enumerate(pratos, start=1):
                            print(f"{nome}, R${valor:.2f} - {i}")
                        while True:
                            selecao_prato = input('Escolha entre as opções disponíveis (o número ao lado do prato): ')
                            if not selecao_prato.isdigit():
                                print('Digite apenas números')
                                continue
                            selecao_prato = int(selecao_prato)-1
                            if not 1<= selecao_prato <= len(pratos):
                                print(f'A opção escolhida não é válida, escolha uma opção entre 1 e {len(pratos)}')
                                continue
                            nome_prato = pratos[selecao_prato][0]
                            prato_escolhido = cursor.execute(f"SELECT id FROM pratos WHERE nome = %s", (nome_prato,))
                            while True:
                                decisao = input(f"Você escolheu o prato {nome_prato}\nDigite SIM caso deseje realizar o pedido\nDigite NÃO caso deseje cancelar o pedido e voltar ao menu\n")
                                if not decisao.isalpha():
                                    print("Digite apenas SIM ou NÃO")
                                    continue
                                if unidecode(decisao.lower()) == "nao":
                                    print("Você será redirecionado ao menu")
                                    time.sleep(1)
                                    menu_f(conexao, cursor)
                                    break
                                if decisao.lower() == "sim":
                                    cursor.execute(f"SELECT valor FROM pratos WHERE id = %s", (prato_escolhido)) # == LEITURA DO VALOR ==
                                    valor_prato = cursor.fetchone()
                                    time.sleep(1)
                                    print(f'O valor do seu pedido é de: R${valor_prato}')
                                    if checar_senha_usuario(conexao, cursor, cpf):
                                        cursor.execute(f'SELECT credito FROM cadastros WHERE cpf = %s', (cpf))
                                        resultado = cursor.fetchone()
                                        if int(resultado) >= int(valor_prato): # == VERIFICAR SE O USUÁRIO POSSUI CRÉDITOS SUFICIENTES ATRAVÉS DE UMA CONSULTA AO BANCO DE DADOS ==
                                            print('Estamos processando...')
                                            time.sleep(1)
                                            credito_desconto = int(resultado) - 45
                                            cursor.execute(f'UPDATE cadastros SET credito = %s WHERE cpf = %s', (credito_desconto, cpf)) # == UPDATE DOS CRÉDITOS SUBTRAIDOS PELO VALOR DO PRATO ==
                                            conexao.commit()
                                            #fazer a adição do ticket
                                            print('Compra realizada com sucesso e Ticket gerado\nEstamos lhe redirecionando para o menu..')
                                            time.sleep(1)

                                        else:
                                            add_credito = True
                                            while add_credito: # == PERGUNTAR AO USUÁRIO SE ELE QUER ADICIONAR CRÉDITOS OU RETORNAR AO MENU ==
                                                decisao_credito = input('Você não tem créditos para realizar essa compra!\nDigite 1 para adicionar créditos ou 2 para retornar ao menu: ')
                                                if decisao_credito == '1':
                                                    add_credito = False
                                                    creditos_add(conexao, cursor) # Pass conexao and cursor
                                                    ver_restaurantes(conexao, cursor) # Pass conexao and cursor
                                                    return # Exit after redirecting to add credits or restaurants
                                                elif decisao_credito == '2':
                                                    print('Você está sendo redirecionado para o menu...')
                                                    time.sleep(1)
                                                    menu_f(conexao, cursor) # Pass conexao and cursor
                                                    return # Exit after redirecting to menu
                                                else:
                                                    print('Tente uma opção válida!')
                                                    continue
                                    else:
                                        print('Senha não válida, tente novamente')
                                        continue
                                        # The loop will continue, asking for password again
                        
                                    menu_f(conexao, cursor) # Pass conexao and cursor
            ver_restaurantes(conexao, cursor) # Pass conexao and cursor



        # == VER TICKET ==
        elif opcao_menu == '4':
            def Ver_ticket(conexao, cursor): # Add conexao and cursor as arguments

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
                        decisao_ticket = input('Deseja retornar ao menu? Digite 1 para retornar ou voltará para o início dessa aba : ')
                        if decisao_ticket == '1':
                            menu_f(conexao, cursor) # Pass conexao and cursor
                            break
                        else:
                            print('Estamos lhe redirecionando para o início dessa aba!')
                            time.sleep(1)
                    else:
                        print('Senha inválida, digite novamente')
                # The loop ends when the user enters '1'
                menu_f(conexao, cursor) # This line will only be reached if the loop breaks, otherwise the inner call to menu_f handles it.
            Ver_ticket(conexao, cursor) # Pass conexao and cursor


        # == DELETAR CONTA ==

        elif opcao_menu == '5':
            def deletar_conta(conexao, cursor): # Add conexao and cursor as arguments

                while True: # Loop for valid CPF input
                    cpf = input('Digite o CPF da conta a ser apagada: ') # == VERIFICAÇÃO POR CPF ==
                    if not cpf.isdigit() or not len(cpf) == 11:
                        print('CPF inválido. Digite exatamente 11 números.')
                        time.sleep(1)
                        continue
                    break

                consulta2 = 'SELECT * FROM cadastros WHERE cpf = %s'
                cursor.execute(consulta2, (cpf,))
                resultado = cursor.fetchone()
                if resultado:
                    print('CPF validado!')
                    time.sleep(1)
                else:
                    while True: # == LOOP PARA SOLICITAR UM CPF VÁLIDO ATÉ O USUÁRIO ACERTAR ==
                        cpf = input('Digite novamente um CPF válido! ')
                        if not cpf.isdigit() or not len(cpf) == 11:
                            print('CPF inválido. Digite exatamente 11 números.')
                            time.sleep(1)
                            continue
                        consulta3 = 'SELECT * FROM cadastros WHERE cpf = %s'
                        cursor.execute(consulta3, (cpf,))
                        resultado = cursor.fetchone()
                        if resultado:
                            print('CPF validado!')
                            time.sleep(1)
                            break # Exit the inner loop once CPF is valid
                        else:
                            print('Escreva seu CPF correto: ')
                            time.sleep(1)
                            continue

                while True: # Loop for valid deletion decision
                    decisao_delete = input('Digite SIM para confirmar a exclusão da conta ou NAO para retornar ao menu: ') # == CONFIRMAÇÃO DE EXCLUSÃO ==
                    if decisao_delete.upper() == 'SIM':
                        comando = 'DELETE FROM cadastros WHERE cpf = %s ' # == DELETE DA CONTA NO BANCO DE DADOS ==
                        cursor.execute(comando, (cpf,))
                        conexao.commit()
                        print('Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial')
                        time.sleep(1)
                        inicio(conexao, cursor) # Redirect to inicio after deletion
                        return # Exit function
                    elif decisao_delete.upper() == 'NAO':
                        print('Você está sendo redirecionado para o menu!')
                        menu_f(conexao, cursor) # Pass conexao and cursor
                        return # Exit function
                    else:
                        print('Tente novamente uma opção válida!')
                        time.sleep(1)
            deletar_conta(conexao, cursor) # Pass conexao and cursor
        elif opcao_menu == '6':
            login(conexao, cursor) # Pass conexao and cursor
        else:
            print('Tente uma opção válida!')
            time.sleep(1)


# == LOGIN ==

def login(conexao, cursor): # Add conexao and cursor as arguments
    #retorna ao login quando quiser
    while True:
        cpf = (input('Qual é o seu CPF (digite apenas os números): '))
        if not cpf.isdigit():
            print('Digite apenas números, no formato (12345678912)') # == VERIFICAR SE HÁ APENAS NÚMEROS ==
            continue
        if not len(str(cpf)) == 11: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DO CPF ==
            print('Digite exatamente 11 números')
            continue
        break # Exit loop if CPF is valid

    while True:
        senha = (input('Qual é sua senha ? '))
        if not senha.isdigit(): # == VERIFICAÇÃO SE HÁ APENAS NÚMEROS ==
            print('Escreva apenas números EX: (1234)')
            continue
        if not len(str(senha)) == 4: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DO CPF ==
            print('Escreva exatamente 4 digitos EX: (1234)')
            continue
        break # Exit loop if password is valid

    checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR EXISTÊNCIA DO CPF NO BANCO DE DADOS ==
    cursor.execute(checagem_cpf, (cpf,)) # Note the comma for tuple
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
                if not (1 <= decisao_senha <= 2): # Simplified range check
                    print('Digite apenas 1 ou 2')
                    continue
                if decisao_senha == 1:
                    login(conexao, cursor)
                    break # Go back to the top of the login function to re-enter password
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
                            continue
                        checagem_codigo = "SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s"
                        cursor.execute(checagem_codigo, (cpf, codigo))
                        resultado = cursor.fetchone()
                        if not resultado:
                            print('Seu código está incorreto, tente novamente')
                            continue
                        senha_recuperada = randint (1000, 9999) # == GERAÇÃO DE SENHA ALEATÓRIA PARA O USUÁRIO APÓS VALIDAÇÃO DE CÓDIGO ==
                        atualizar = "UPDATE cadastros SET senha = %s WHERE cpf = %s" # == UPDATE NO BANCO DE DADOS ==
                        cursor.execute(atualizar, (senha_recuperada, cpf))
                        conexao.commit()
                        print(f'Agora sua nova senha é {senha_recuperada}\nGuarde sua senha\nAgora você será direcionado ao login')
                        login(conexao, cursor) # Call login with connection and cursor
                        return # Exit the function after successful recovery
                continue # Continue the outer loop to re-enter password
        else:
            print('Você fez o login com sucesso')
            menu_f(conexao, cursor) # Pass conexao and cursor # == IDA AO MENU ==
            return # Exit login function after successful login
    else:
        print('Seu CPF está errado')
        while True: # == OPÇÃO AO USUÁRIO DE TENTAR NOVAMENTE DIGITAR O CPF OU CADASTRAR UMA NOVA CONTA ==
            logado = input('Se você tiver apenas digitado seu CPF errado: digite 1\nSe você não tiver conta, para ser redirecionado ao cadastro: digite 2\nO que você deseja ?: ')
            if not logado.isdigit():
                print('Digite apenas 1 ou 2')
                continue
            logado = int(logado)
            if not (1 <= logado <= 2):
                print('Digite apenas 1 ou 2')
                continue
            break # Exit loop if input is valid
        if logado == 1:
            print('Você será redirecionado para o login novamente')
            login(conexao, cursor) # Pass conexao and cursor # == TENTAR LOGAR NOVAMENTE ==
            return # Exit function
        if logado == 2:
            cadastro(conexao, cursor) # Pass conexao and cursor
            return # Exit function

# == CADASTRO == :

def cadastro(conexao, cursor): # Add conexao and cursor as arguments
    print('Vamos fazer seu cadastro')
    while True:
        cpf = input('Informe seu CPF: ')
        if not cpf.isdigit(): # == INFORMAR UM CPF VÁLIDO DE ACORDO COM A QUANTIDADE DE NÚMEROS E SE HÁ APENAS NÚMEROS ==
            print('Escreva apenas números EX: (01234567891)')
            continue
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
            if not (1 <= logado2 <= 2):
                print('Digite apenas "1" ou "2"')
                continue
            if logado2 == 1:
                login(conexao, cursor) # Pass conexao and cursor
                return # Exit function
            if logado2 == 2:
                cadastro(conexao, cursor) # Pass conexao and cursor
                return # Exit function
    while True:
        senha = input('Qual vai ser sua senha ?\nA senha deve conter exatamente 4 números: ')
        if not senha.isdigit():
            print('Escreva apenas números, no formato (1234)')
            continue # == CRIAÇÃO DE SENHA ATRAVÉS DOS FORMATOS VÁLIDOS ( APENAS NÚMEROS E 4 DÍGITOS ) ==
        if not len(str(senha)) == 4:
            print('Escreva exatamente 4 números, no formato (1234)')
            continue
        break
    codigo = randint(10000, 99999) # Changed range to ensure 5 digits
    # Use parameterized query for INSERT
    adicionar = 'INSERT INTO cadastros (cpf, senha, codigo, credito, ticketpizzaria, tickethamburgueria, ticketcomidabr) VALUE (%s, %s, %s, 0, 0, 0, 0)'
    cursor.execute(adicionar, (cpf, senha, codigo))
    conexao.commit()
    print(f'\033[31mFOI CRIADO UM CÓDIGO PESSOAL PARA VOCÊ USAR EM CASO DE RECUPERAÇÃO DE SENHA, NÃO O PERCA!\nSEU CÓDIGO É {codigo}\033[0m')
    print('Você foi cadastrado com sucesso!\nAgora você retornará ao login, e escreva seus dados cadastrados')
    login(conexao, cursor) # Pass conexao and cursor # == IDA AO LOGIN PARA ENTRAR NA SUA CONTA ==
    return # Exit function

def checar_senha_usuario(conexao, cursor, cpf, senha_checagem):
    while True:
        senha_checagem = input("Defina sua senha (a senha deve conter 4 números EX: 1234: )")
        if not senha_checagem.isdigit():
            print('Escreva apenas números, no formato (1234)')
            continue
        if not len(str(senha_checagem)) == 4:
            print('Escreva exatamente 4 números, no formato (1234)')
            continue
        break
    cursor.execute(f'SELECT senha FROM cadastros WHERE cpf = %s', (cpf))
    senha_certa = cursor.fetchone()
    if senha_checagem == senha_certa:
        return True
    else: return False

def validar_modelo_email(email):
    try:
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)