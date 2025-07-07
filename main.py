import funcoes_fastake as fk
import mysql.connector
import time
from usuario import Usuario
from usuario import inicio
from restaurantes import Restaurantes
from random import randint
import sessao

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake'
)
cursor = conexao.cursor()

while True:
    global usuario
    inicio = input('=== Bem vindo à Fastake!! ===\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
    if inicio == '1':
        print(' === Bem-vindo à aba de cadastro ===')
        sessao.usuario_cadastrado = Usuario.cadastrar()

    elif inicio == '2':
        login = True
        while login:
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            sessao.usuario_logado = Usuario.fazer_login()
            time.sleep(1)
            break
           
        while True:
            opcoes_menu = (
            '1 - Trocar senha'
            '\n2 - Ver crédito'
            '\n3 - Ver restaurantes'
            '\n4 - Ver tickets'
            '\n5 - Deletar conta'
            '\n6 - Ir para página de login'
            )
            opcao_menu = input(str(f' === Menu ===:\n{opcoes_menu}\nDigite aqui uma opção válida: '))
                # == TROCAR SENHA ==
            if opcao_menu == '1':
                sessao.usuario_logado.trocar_senha()

            # == VER CRÉDITO ==
            elif opcao_menu == '2': 
                sessao.usuario_logado.creditos_ver()
                
            # == VER RESTAURANTES ==

            elif opcao_menu == '3':
                r = Restaurantes("placeholder", "placeholder")  # Instância qualquer para acessar o método
                r.ver_restaurantes()

                #Restaurantes.ver_restaurantes()
                #usuario_logado.ver_restaurantes(conexao, cursor)
                

            # == VER TICKET ==
            elif opcao_menu == '4': # EM DESENVOLVIMENTO
                sessao.usuario_logado.ver_tickets()
                time.sleep(1)
                #menu

            # == DELETAR CONTA ==

            elif opcao_menu == '5':
                sessao.usuario_logado.deletar_conta()
                
            elif opcao_menu == '6':
                time.sleep(1)
                break
            else:
                print('Digite uma opção válida!')
                time.sleep(1)
                continue
    else:
        print('Digite uma opção válida!')
        time.sleep(1)
        continue
