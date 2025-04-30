import mysql.connector
from random import randint
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'fastake',
)
cursor = conexao.cursor()
print('Bem vindo!\nPor favor preencha os campos abaixo para prosseguir:')
#login inicio
valores = [] 
def menu():
    print('Você está no menu')   
def login():
    #retorna ao login quando quiser
    while True:
        CPF = input('Qual é o seu cpf (digite apenas os números): ')
        if not CPF.isdigit():
            print('Digite apenas números, no formato (12345678912)')
            continue
        CPF = int(CPF)
        if not len(str(CPF)) == 11:
            print('Digite exatamente 11 números')
            continue
        #fazer a verificação mais complicada da combinação dos números do CPF
        break
    while True:
        SENHA = input('Qual é sua senha ? ')
        if not SENHA.isdigit():
            print('Escreva apenas números EX: (1234)')
            continue
        SENHA = int(SENHA)
        if not len(str(SENHA)) == 4:
            print('Escreva exatamente 4 digitos EX: (1234)')
            continue
        checagem_cpf = "SELECT CPF FROM cadastro WHERE CPF = %s"
        cursor.execute(checagem_cpf, (CPF,))
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            checagem_senha = "SELECT * FROM cadastro WHERE CPF = %s AND SENHA = %s"
            cursor.execute(checagem_senha, (CPF, SENHA))
            resultado = cursor.fetchone()
            if not resultado:
                while True:
                    decisao_senha = input('Sua senha está errada, deseja tentar novamente ?\nSe desejar tentar novamente digite 1, se desejar recuperar senha digite 2:  ')
                    if not decisao_senha.isdigit() or 2 >= decisao_senha or decisao_senha >= 1:
                        print('digite apenas 1 ou 2')
                        continue
                    decisao_senha = int(decisao_senha)
                    if decisao_senha == 1:
                        break
                    if decisao_senha == 2:
                        print('Você será redirecionado para recuperar a sua senha')
                        while True:
                            codigo_teste = input('Informe seu código pessoal para recuperar sua senha: ')
                            if not codigo_teste.isdigit() or len(codigo_teste) == 5:
                                print('Digite apenas números, com 4 digitos EX: (12345)')
                                continue
                            codigo_teste = int(codigo_teste)
                            checagem_codigo = f'SELECT * FROM cadastro WHERE CPF = {CPF} AND CODIGO = {codigo_teste} '
                            cursor.execute(checagem_codigo, (CPF, SENHA))
                            resultado = cursor.fetchone()
                            if not resultado:
                                print('Seu código está incorreto, digite no formato (12345)')
                                continue
                            SENHA = randint (1000, 10000)
                            atualizar = "UPDATE cadastro SET SENHA = %s WHERE CPF = %s"
                            cursor.execute(atualizar)
                            print(f'Agora sua nova senha é {SENHA}\nGuarde sua senha\nAgora você será direcionado ao login')
                            login()
                            break
                        exit()
                continue
            else:
                print('Você fez o login com sucesso')
                menu()
                exit()
        else:
            print('Seu CPF está errado')
            while True:
                logado = input('Se você tiver apenas digitado seu CPF errado: digite 1\nSe você não tiver conta, para ser redirecionado ao cadastro: digite 2\nO que você deseja ?: ')
                if not logado.isdigit():
                    print('Digite apenas 1 ou 2')
                    continue
                logado = int(logado)
                if not logado >= 1 and logado <=2 :
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
                        CPF = input('Informe seu CPF: ')
                        if not CPF.isdigit():
                            print('Escreva apenas números EX: (01234567891)')
                            continue
                        CPF = int(CPF)
                        if not len(str(CPF)) == 11:
                            print('Escreva 11 números EX: (01234567891)')
                            continue
                        break
                    checagem_cpf = "SELECT CPF FROM cadastro WHERE CPF = %s"
                    cursor.execute(checagem_cpf, (CPF,))
                    resultado = cursor.fetchall()
                    if resultado != 0 :
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
                        SENHA = input('Qual vai ser sua senha ?\nA senha deve conter exatamente 4 números: ')
                        if not SENHA.isdigit():
                            print('Escreva apenas números, no formato (1234)')
                            continue
                        SENHA = int(SENHA)
                        if not len(str(SENHA)) == 4:
                            print('Escreva exatamente 4 números, no formato (1234)')
                            continue
                        break
                    CODIGO = randint(10000, 100000)
                    adicionar = f'INSERT INTO cadastro (CPF, SENHA, CODIGO) VALUE ({CPF}, {SENHA}, {CODIGO})'
                    cursor.execute(adicionar)
                    conexao.commit()
                    #com cadastro criado voltará ao login
                    print(f'\033[31mFOI CRIADO UM CÓDIGO PESSOAL PARA VOCÊ USAR EM CASO DE RECUPERAÇÃO DE SENHA, NÃO O PERCA!\nSEU CÓDIGO É {CODIGO}\033[0m')
                    print('Você foi cadastrado com sucesso!\nAgora você retornará ao login, e escreva seus dados cadastrados')
                    login()
                    exit()
                cadastro()
login()
#MENU
     
cursor.close()
conexao.close()