import mysql.connector

from random import randint
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake_project',
)
cursor = conexao.cursor()
#CONSULTAS:
cursor.execute('SELECT cpf, senha, codigo, credito FROM cadastros')
dados = cursor.fetchall()
print('Bem vindo!\nPor favor preencha os campos abaixo para prosseguir:')
#login inicio
valores = []

#MENU!!!
def menu_f():
    menu = True
    import time
    import mysql.connector
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '2710',
        database = 'fastake_project',
    )
    cursor = conexao.cursor()

    opcoes_menu = (
    '1 - Trocar senha'
    '\n2 - Ver crédito'
    '\n3 - Ver restaurantes'
    '\n4 - Ver tickets'
    '\n5 - Deletar conta'
    )
    while menu:
        opcao_menu = input(str(f'Menu:\n{opcoes_menu}\nDigite aqui uma opção válida: '))
        #TROCAR SENHA

        if opcao_menu == '1':
            codigo_trocar = int(input('Digite seu código de segurança: '))
            consulta = 'SELECT * FROM cadastros WHERE codigo = %s'
            cursor.execute(consulta, (codigo_trocar,))
            resultado = cursor.fetchone()
            if resultado:
                print('Seu código foi validado com sucesso!')
                time.sleep(1)
                try:
                    nova_senha = int((input('Digite aqui sua nova senha (4 dígitos): ')))
                    if 999 < nova_senha < 10000:
                        comando_novasenha = f'UPDATE cadastros SET senha = %s WHERE codigo = %s'
                        cursor.execute(comando_novasenha, (nova_senha, codigo_trocar))
                        conexao.commit()
                        time.sleep(1)
                        print('Senha salva com sucesso!,\nVocê está sendo redirecionado para o menu')
                        time.sleep(1)
                        menu = True
                    else:
                        raise ValueError
                except ValueError:
                        print('Senha inválida!')
                        time.sleep(1)
                        senha_invalida = True
                        while senha_invalida:
                            try:
                                nova_senha2 = int(input('Tente novamente: '))
                                if nova_senha2 > 999 and nova_senha2 < 10000:
                                    time.sleep(1)
                                    comando_novasenha2 = f'UPDATE cadastros SET senha = {nova_senha2} WHERE codigo = %s'
                                    cursor.execute(comando_novasenha2, (codigo_trocar))
                                    conexao.commit()
                                    print('Senha salva com sucesso!')
                                    #Armazenar no mysql
                                    time.sleep(1)
                                    print('Você está sendo redirecionado para o menu!')
                                    time.sleep(1)
                                    senha_invalida = False
                                    menu = True
                                else:
                                    print('Senha deve ter 4 dígitos!')
                                    senha_invalida = True
                            except ValueError:
                                print('Você deve digitar apenas números')
            else:
                print('Código inválido, tente novamente')
                time.sleep(1)
                menu = True
    # VER CRÉDITO
        elif opcao_menu == '2':
            while True:
                consulta_senha = input('Digite sua senha para continuar: ')
                print('Estamos carregando seu saldo de créditos...')
                time.sleep(1)

                consulta_credito = 'SELECT credito FROM cadastros WHERE senha = %s'
                cursor.execute(consulta_credito, (consulta_senha,))
                resultado = cursor.fetchone()

                if resultado:
                    credito_atual = int(resultado[0])
                    print(f'Você tem {credito_atual} créditos')
                    time.sleep(1)

                    add = input('Você deseja adicionar mais créditos? Digite SIM para adicionar: ')
                    if add.upper() == 'SIM':
                        quantia = int(input('Digite a quantia desejada, em R$: '))
                        quantia_nova = credito_atual + quantia

                        forma_pagamento = input('Qual será a forma de pagamento? ')
                        print(f'Estamos processando sua solicitação de acordo com a forma escolhida ({forma_pagamento})...')
                        time.sleep(1)
                        #FAZER OPÇÃO 1,2,3 EM FORMA DE PAGAMANTO ( PIX, CRÉDITO OU DÉBITO )
                        adicionar_quantia = 'UPDATE cadastros SET credito = %s WHERE senha = %s'
                        cursor.execute(adicionar_quantia, (quantia_nova, consulta_senha))
                        conexao.commit()

                        print('Processo finalizado com sucesso!')
                        time.sleep(1)
                    else:
                        print('Você está sendo redirecionado para o menu...')
                        time.sleep(1)

                    break  # Sai do loop após operação bem-sucedida
                else:
                    print('Senha inválida. Tente novamente.\n')

            menu_f()
        
         
        #VER RESTAURANTES

        elif opcao_menu == '3':
            print('Estamos lhe redirecionando para a página de restaurantes participantes!')
            time.sleep(1)
            opcoes = 'SELECT * FROM restaurantes'
            cursor.execute(opcoes)
            resultado = cursor.fetchall()
            print(f'Restaurante 1 = {resultado[0]}\nRestaurante 2 = {resultado[1]}\nRestaurante 3 = {resultado[1]}')
            
            escolha = input('Escolha entre as três opções disponíveis:\nDigite 1 , 2 ou 3: ')
             
            

        #VER TICKET
        elif opcao_menu == '4':
            print('Ver ticket')
            menu = False
        #DELETAR CONTA
        elif opcao_menu == '5':
            cpf = int(input('Digite o CPF da conta a ser apagada: '))
            consulta2 = 'SELECT * FROM cadastros WHERE cpf = %s'
            cursor.execute(consulta2, (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                print('CPF validado!')
                time.sleep(1)
            else:
                while True:
                    cpf2 = int(input('Digite novamente um CPF válido!'))
                    consulta3 = 'SELECT * FROM cadastros WHERE cpf = %s'
                    cursor.execute(consulta3, (cpf2,))
                    resultado = cursor.fetchone()
                    if resultado:
                        print('CPF validado!')
                        time.sleep(1)
                        False
                    else:
                        print('Escreva seu CPF correto: ')
                        time.sleep(1) 
                        continue  
            decisao_delete = str(input('Digite SIM para confirmar a exclusão da conta: '))
            decisao_invalida = True
            if decisao_delete.upper() == 'SIM':
                comando = 'DELETE FROM cadastros WHERE cpf = %s '
                cursor.execute(comando, (cpf2,))
                conexao.commit()
                print('Conta deletada com sucesso!\n Você está sendo redirecionado para a página de login')
                time.sleep(1)
            else:
                while decisao_invalida:
                    decisao_delete2 = str(input('Digite SIM para confirmar a exclusão da conta: '))
                    if decisao_delete2.upper() == 'SIM':
                        comando = 'DELETE FROM cadastros WHERE cpf = %s'
                        cursor.execute(comando, (cpf,))
                        conexao.commit()
                        print('Conta deletada com sucesso!\n Você está sendo redirecionado para a página de login ')
                        time.sleep(1)
                        break
                    else:
                        print('Tente novamente')
                        time.sleep(1)
        
            #delete, DELETE ( DELETE FROM cadastros WHERE cpf = "{cpf}")
            # cadastros = tabela-alvo
            # cpf = coluna-alvo e onde apagar
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
            print('Digite apenas números, no formato (12345678912)')
            continue
        cpf = int(cpf)
        if not len(str(cpf)) == 11:
            print('Digite exatamente 11 números')
            continue
        #fazer a verificação mais complicada da combinação dos números do CPF
        break
    while True:
        senha = (input('Qual é sua senha ? '))
        if not senha.isdigit():
            print('Escreva apenas números EX: (1234)')
            continue
        senha = int(senha)
        if not len(str(senha)) == 4:
            print('Escreva exatamente 4 digitos EX: (1234)')
            continue
        checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s"
        cursor.execute(checagem_cpf, (cpf,))
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            checagem_senha = "SELECT * FROM cadastros WHERE cpf = %s AND senha = %s"
            cursor.execute(checagem_senha, (cpf, senha))
            resultado = cursor.fetchone()
            if not resultado:
                while True:
                    decisao_senha = input('Sua senha está errada, deseja tentar novamente ?\nSe desejar tentar novamente digite 1, se desejar recuperar senha digite 2:  ')
                    if not decisao_senha.isdigit():
                        print('digite apenas 1 ou 2')
                        continue
                    decisao_senha = int(decisao_senha)
                    if not 2 >= decisao_senha or decisao_senha >= 1:
                        print('Digite apenas 1 ou 2')
                    if decisao_senha == 1:
                        break
                    if decisao_senha == 2:
                        print('Você será redirecionado para recuperar a sua senha')
                        while True:
                            codigo = input('Informe seu código pessoal para recuperar sua senha: ')
                            if not codigo.isdigit():
                                print('Digite apenas números, com 5 digitos EX: (12345)')
                                continue
                            codigo = int(codigo)
                            if not len(str(codigo)) == 5:
                                print('Digite apenas números, com 5 digitos EX: (12345)')
                            checagem_codigo = "SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s"
                            cursor.execute(checagem_codigo, (cpf, codigo))
                            resultado = cursor.fetchone()
                            if not resultado:
                                print('Seu código está incorreto, tente novamente')
                                continue
                            senha = randint (1000, 10000)
                            atualizar = "UPDATE cadastros SET senha = %s WHERE cpf = %s"
                            cursor.execute(atualizar, (senha, cpf))
                            conexao.commit()
                            print(f'Agora sua nova senha é {senha}\nGuarde sua senha\nAgora você será direcionado ao login')
                            login()
                            break
                        exit()
                continue
            else:
                print('Você fez o login com sucesso')
                menu_f()
                exit()
        else:
            print('Seu CPF está errado')
            while True:
                logado = input('Se você tiver apenas digitado seu CPF errado: digite 1\nSe você não tiver conta, para ser redirecionado ao cadastro: digite 2\nO que você deseja ?: ')
                if not logado.isdigit():
                    print('Digite apenas 1 ou 2')
                    continue
                logado = int(logado)
                if not logado >= 1 and logado <= 2:
                    print('Digite apenas 1 ou 2')
                    continue
                break
            if logado == 1:
                print('Você será redirecionado para o login novamente')
                login()
                exit()
            if logado == 2:
                def cadastro():
                    #vai para a parte de cadastro quando precisar
                    print('Vamos fazer seu cadastro')
                    while True:
                        cpf = input('Informe seu CPF: ')
                        if not cpf.isdigit():
                            print('Escreva apenas números EX: (01234567891)')
                            continue
                        cpf = int(cpf)
                        if not len(str(cpf)) == 11:
                            print('Escreva 11 números EX: (01234567891)')
                            continue
                        break
                    checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s"
                    cursor.execute(checagem_cpf, (cpf,))
                    resultado = cursor.fetchall()
                    if len(resultado) != 0:
                        print('Esse CPF já está cadastrado')
                        while True:
                            logado2 = input('Digite 1, se você já tem login\nDigite 2 caso tenha digitado errado e queira repetir: ')
                            if not logado2.isdigit():
                                print('Digite apenas "1" ou "2"')
                                continue
                            logado2 = int(logado2)
                            if not logado2 >= 1 and logado2 <= 2:
                                print('Digite apenas "1" ou "2"')
                                continue
                            if logado2 == 1:
                                login()
                                exit()
                                break
                            if logado2 == 2:
                                cadastro()
                                exit()
                                break
                            break
                    while True:
                        senha = input('Qual vai ser sua senha ?\nA senha deve conter exatamente 4 números: ')
                        if not senha.isdigit():
                            print('Escreva apenas números, no formato (1234)')
                            continue
                        senha = int(senha)
                        if not len(str(senha)) == 4:
                            print('Escreva exatamente 4 números, no formato (1234)')
                            continue
                        break
                    codigo = randint(999, 10000)
                    adicionar = f'INSERT INTO cadastros (cpf, senha, codigo) VALUE ({cpf}, {senha}, {codigo})'
                    cursor.execute(adicionar)
                    conexao.commit()
                    #com cadastro criado voltará ao login
                    print(f'\033[31mFOI CRIADO UM CÓDIGO PESSOAL PARA VOCÊ USAR EM CASO DE RECUPERAÇÃO DE SENHA, NÃO O PERCA!\nSEU CÓDIGO É {codigo}\033[0m')
                    print('Você foi cadastrado com sucesso!\nAgora você retornará ao login, e escreva seus dados cadastrados')
                    login()
                    exit()
                cadastro()
login()




#FUNCAO MENU!!



