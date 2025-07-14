
import mysql.connector
import time
from random import randint
from unidecode import unidecode
from adm import Admin
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake'
)
cursor = conexao.cursor()

class Checagem:

    ''' Classe para armarzenar os métodos de checagem de dados ( cpf, senha e código ) existentes ao longo do sistema, através de restrições e validações '''


    def checar_cpf(self, cpf):

        ''' Checar o CPF no processo de logi/cadastro, antes de outras possibilidades do usuário, como , ao rrar, ter a possibilidade de tentar
        novamente ou ir para a aba inicial '''

        while True:
            if not cpf.isdigit():
                print('Digite apenas números, no formato (12345678912)') # == VERIFICAR SE HÁ APENAS NÚMEROS ==
                continue
            cpf = int(cpf)
            if not len(str(cpf)) == 11: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DO CPF ==
                print('Digite exatamente 11 números')
                continue
            break
                
    def checar_codigo(self, codigo, cpf):

        ''' Checagem do código de acordo com certos critérios, como tamanho do mesmo e se possui apenas dígitos '''

        cod = True
        while cod:
            if not str(codigo).isdigit() or len(str(codigo)) != 4:
                print('Código inválido, tente novamente!')
                while True:
                    codigo = input('Digite aqui novamente: ')
                    if not str(codigo).isdigit() or len(str(codigo)) != 4:
                        print('Código inválido, tente novamente!')
                    codigo = int(codigo)
                    cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
                    if not cursor.fetchone():
                        print('Código incorreto.')
                        continue
                    cod = False
                    break
            
            codigo = int(codigo)
            cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
            while True:
                if not cursor.fetchone():
                    print('Código incorreto, tente novamente!')
                    codigo = input('Digite aqui: ')
                    codigo = int(codigo)
                    cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
                    if not cursor.fetchone():
                        print('Tente novamente!')
                        continue
                cod = False
                break   

    def checar_senha_login(self, senha):

        ''' Checar a senha no ato de login, para verificar se há apenas dígitos e analisar o tamanho da senha '''

        while True:
            if not str(senha).isdigit() or len(str(senha)) != 4:
                    print('Senha inválida. Tente novamente!')
                    while True:
                        senha = input('Digite aqui: ')
                        if not str(senha).isdigit() or len(str(senha)) != 4:
                            print('Tente novamente!')
                            continue
                        break
            senha = int(senha)
            break

    def checar_senha_cadastro(self, senha):

        ''' Checar as restrições de uma senha no ato de cadastro, para analisar se estão de acordo '''

        while True:
            if not str(senha).isdigit() or len(str(senha)) != 4:
                    print('Senha inválida! Deve conter exatamente 4 dígitos numéricos.')
                    continue
            senha = int(senha)
            break

    def checar_senha_compra(conexao, cpf):

        ''' Checagem de senha realizada no ato da compra de um produto em certo restaurante '''

        while True:
            senha_checagem = int(input('Digite sua senha para continuar: '))
            if not str(senha_checagem).isdigit():
                print('Escreva apenas números, no formato (1234)')
                continue
            if not len(str(senha_checagem)) == 4:
                print('Escreva exatamente 4 números, no formato (1234)')
                continue
            break
        cursor.execute(f'SELECT senha FROM cadastros WHERE cpf = %s', (cpf,))
        senha_certa = cursor.fetchone()
        if senha_checagem == int(senha_certa[0]):
            return True
        else: 
            return False

check = Checagem()


class Usuario:

    ''' Classe para armazenar os objetos do usuário instanciado, bem como as suas possibilidades de ações dentro do programa
    como fazer login ; cadastrar ou até mesmo deletar a conta, abrangendo um CRUD completo '''

    def __init__(self, cpf, senha, codigo):
        self.cpf = cpf
        self.senha = senha
        self.codigo = codigo

    @classmethod
    def fazer_login(cls):

        ''' Login de um usuário já cadastrado '''

        print('Bem-vindo à página de login! Vamos começar : ')
        login = True
        while login: 
            while True:
                cpf = input('Digite seu CPF (somente números): ')
                check.checar_cpf(cpf)
                checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR EXISTÊNCIA DO CPF NO BANCO DE DADOS ==
                cursor.execute(checagem_cpf, (cpf,))
                resultado = cursor.fetchall()
                if resultado:
                    print(f'CPF validado!')
                else:
                    while True:
                        decisao = input(f'CPF não existente, digite 1 para ir até a aba inicial: ')
                        if decisao == '1':
                            inicio()
                            login = False
                            break
                        else:
                            print('Digite apenas "1"!')
                            continue
                break
            
            while True:
                codigo = input('Digite seu código de segurança (4 dígitos): ')
                check.checar_codigo(codigo, cpf)
                break

            while True:
                senha = input('Digite aqui sua senha ( 4 números ): ')
                check.checar_senha_login(senha)
                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND senha = %s', (cpf, senha))
                if not cursor.fetchone():
                    decisao = True
                    while decisao: 
                        decisao_senha = int(input('Senha incorreta, você esqueceu sua senha? Digite 1 para recupera-la ou 2 para tentar novamente: '))
                        if decisao_senha == 1:
                            cls.recuperar_senha(cls)
                            decisao = False
                            break
                        elif decisao_senha == 2:
                            tentativa = True
                            while tentativa:
                                senha = input('Digite aqui: ')
                                senha = int(senha)
                                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND senha = %s', (cpf, senha))
                                if not cursor.fetchone():
                                    continue
                                tentativa = False
                                decisao = False
                        else:
                            print('Digite uma opção válida!')
                            time.sleep(1)
                            continue
                break

            print('Login realizado com sucesso!')
            login = False
            return cls(cpf, senha, codigo)
    
    @classmethod
    def cadastrar(cls):

        ''' Cadastro do usuário '''

        time.sleep(1)
        cadastro = True
        while cadastro:
            while True:
                cpf = input('Digite aqui seu CPF: ')
                check.checar_cpf(cpf)
                cpf = int(cpf)
                # Verificar se CPF já existe
                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s', (cpf,))
                if cursor.fetchone():
                    print('Este CPF já está cadastrado. Tente fazer login.\nEstamos lhe redirecionando para a página inicial...')
                    time.sleep(1)
                    inicio()
                    cadastro = False
                break

            while True:
                senha = input('Digite sua senha (4 dígitos): ')
                check.checar_senha_cadastro(senha)
                break

            codigo = randint(999, 10000)
            print(f'Seu código de segurança foi gerado : {codigo}\nGuarde-o de forma segura para realizar próximas ações dentro do nosso sistema!')
            time.sleep(1)
            # Inserir no banco
            cursor.execute(
                'INSERT INTO cadastros (cpf, senha, codigo) VALUES (%s, %s, %s)',
                (cpf, senha, codigo)
            )
            conexao.commit()
            print('Cadastro realizado com sucesso! Estamos lhe redirecionando para a página inicial!')

            # Retorna a instância de Usuario
            return cls(cpf, senha, codigo)
    
    def trocar_senha(self):

        ''' Método específico para a troca de senha pelo usuário através de seu código de segurança gerado no cadastro '''

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
                                    verificacao_codigo = False
                                else:
                                    print('Senha deve ter 4 dígitos!')
                                    senha_invalida = True
                            except ValueError:
                                print('Você deve digitar apenas números')
            else:
                print('Código inválido, tente novamente')
                time.sleep(1)

    def deletar_conta(self):

        ''' Deletar a conta do usuário do sistema a partir de uma verificação de CPF '''

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
        decisao_delete = str(input('Digite SIM para confirmar a exclusão da conta ou NAO para retornar ao menu: ')) # == CONFIRMAÇÃO DE EXCLUSÃO ==
        decisao_invalida = True
        if decisao_delete.upper() == 'SIM':
            comando = 'DELETE FROM cadastros WHERE cpf = %s ' # == DELETE DA CONTA NO BANCO DE DADOS ==
            cursor.execute(comando, (cpf,))
            conexao.commit()
            print('Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial')
            time.sleep(1)
            inicio()
        elif decisao_delete.upper() == 'NAO':
            print('Você está sendo redirecionado para o menu!')
            time.sleep(1)
        else:
            print('Tente novamente uma opção válida!')
            time.sleep(1)
            while decisao_invalida:
                decisao_delete2 = str(input('Digite SIM para confirmar a exclusão da conta ou NAO para retornar ao menu! '))
                if decisao_delete2.upper() == 'SIM':
                    comando = 'DELETE FROM cadastros WHERE cpf = %s'
                    cursor.execute(comando, (cpf,)) # == DELETE DA CONTA NO BANCO DE DADOS ==
                    conexao.commit()
                    print('Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial ')
                    inicio()
                    time.sleep(1)
                    decisao_invalida = False
                    break
                elif decisao_delete2.upper() == 'NAO':
                    print('Você está sendo redirecionado para o menu!')
                    time.sleep(1)
                    decisao_invalida = False
                    break
                else:
                    print('Tente novamente uma opção válida!')
                    time.sleep(1)

    def creditos_ver(self):
            
            ''' Carregamento e impressão dos créditos do usuário, bem como a possível adição de créditos caso  o mesmo deseje '''

            print('Estamos carregando seu saldo de créditos...')
            time.sleep(1)
            consulta_credito = 'SELECT credito FROM cadastros WHERE cpf = %s' # == ANÁLISE DO CRÉDITO QUE O USUÁRIO POSSUI NO BANCO DE DADOS ==
            cursor.execute(consulta_credito, (self.cpf,))
            resultado = cursor.fetchone()
            credito_atual = float(resultado[0]) # == IMPRIME O NÚMERO DE CRÉDITOS ==
            print(f'Você tem {credito_atual} créditos')
            time.sleep(1)

            add = input('Você deseja adicionar mais créditos? Digite SIM para adicionar: ')
            if add.upper() == 'SIM':
                quantia = float(input('Digite a quantia desejada, em R$: \n'))
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
                adicionar_quantia = 'UPDATE cadastros SET credito = %s WHERE cpf = %s' # == UPDATE DE CRÉDITOS NO BANCO DE DADOS ==
                cursor.execute(adicionar_quantia, (quantia_nova, self.cpf))
                conexao.commit()
                print('Processo finalizado com sucesso!')
                time.sleep(1)
            else:
                print('Você está sendo redirecionado para o menu...')
                time.sleep(1)

    def recuperar_senha(self):

        ''' Recuperação de senha realizada no processo de login, caso o usuário se esqueça de sua credencial '''

        while True: # == RECUPERAÇÃO DE SENHA ATRAVÉS DO CÓDIGO PESSOAL ==
            codigo = input('Informe seu código pessoal para recuperar sua senha: ')
            if not codigo.isdigit(): # == VERIFICAÇÃO SE HÁ APENAS NÚMEROS ==
                print('Digite apenas números, com 5 digitos EX: (12345)')
                continue
            codigo = int(codigo)
            if not len(str(codigo)) == 4: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS ==
                print('Digite apenas números, com 4 digitos EX: (1234)')
            checagem_codigo = "SELECT * FROM cadastros WHERE codigo = %s"
            cursor.execute(checagem_codigo, (codigo,))
            resultado = cursor.fetchone()
            if not resultado:
                print('Seu código está incorreto, tente novamente')
                continue
            senha = randint (1000, 10000) # == GERAÇÃO DE SENHA ALEATÓRIA PARA O USUÁRIO APÓS VALIDAÇÃO DE CÓDIGO ==
            atualizar = "UPDATE cadastros SET senha = %s WHERE codigo = %s" # == UPDATE NO BANCO DE DADOS ==
            cursor.execute(atualizar, (senha, codigo))
            conexao.commit()
            print(f'Agora sua nova senha é {senha}\nGuarde sua senha\nAgora você será direcionado ao login')
            time.sleep(1)
            #self.fazer_login()
            inicio()
            break

    def ver_tickets(self):

        ''' Impressão dos tickets de forma organizada e relacionada com o usuário, o ID do prato e o código gerado aleatoriamente '''

        print(' === Estamos carregando seus tickets... ===\n')
        time.sleep(1)
        cursor.execute('SELECT id FROM cadastros WHERE cpf = %s', (self.cpf,))
        id_usuario = cursor.fetchone()[0] # Recebimento do id do usuário
        cursor.execute('SELECT tickets.codigo, pratos.nome FROM tickets JOIN pratos ON tickets.id_prato = pratos.id WHERE tickets.id_usuario = %s', (id_usuario,))
        tickets = cursor.fetchall()
        if tickets:
            print(' === Seus Tickets Gerados === ')
            for codigo, nome_prato in tickets:
                print(f'Ticket: {codigo} | Prato: {nome_prato}')
            while True:
                decisao = input('Digite 1 quando quiser retornar ao menu: ')
                if decisao == '1':
                    print('Estamos lhe redirecionando para o menu!')
                    time.sleep(1)
                    break
                else:
                    print('Digite apenas "1"!')
                    continue

        else:
            print('Você ainda não possui tickets registrados.')
            return







def user(): # Add cursor as an argument
    user = True
    while user:
        escolha = input('Bem vindo usuário!\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
        if escolha == '1':
            print('Você está sendo redirecionado para o cadastro!')
            time.sleep(1)
            Usuario.cadastrar() # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            Usuario.fazer_login() # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue


def inicio():
    while True:
        escolha = input("Bem vindo à Fastake!\n" \
        "Se deseja ir para a parte de adiministradores: digite 1\n" \
        "Se deseja ir para a parte de usuários: digite 2\n")
        if escolha == '1':
            print('Você está sendo redirecionado para a página de administrador!')
            time.sleep(1)
            Admin.adm() # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para a página de usuário!')
            time.sleep(1)
            user() # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue


