
import mysql.connector
import time
from random import randint
import funcoes_fastake as fk
from email_validator import EmailNotValidError, validate_email


conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake'
)
cursor = conexao.cursor()



class Admin:
    def __init__(self, email, senha, codigo):
        self.email = email
        self.senha = senha
        self.codigo = codigo

    def validar_email(self, email_checagem):
        cursor.execute(f"SELECT email FROM adm_nova WHERE email = %s", (email_checagem,))
        resultado = cursor.fetchone()
        return bool(resultado)
        
    def checar_senha_adm(self, senha):
        while True:
            if not senha.isdigit():
                print('Escreva apenas números, no formato (1234)')
                continue
            if not len(senha) == 4:
                print('Escreva exatamente 4 números, no formato (1234)')
                continue
            break
        return senha
    @classmethod
    def cadastro_adm(cls):
        email = True
        while email:
            print('Vamos realizar seu cadastro!\nPor favor preencha os dados abaixo')
            email_checagem = input("Defina seu email: ")
            if not cls.validar_modelo_email(email_checagem):
                print("Digite seu email corretamente")
                continue
            break
        senha_check = True
        while senha_check:
            senha = input("Defina sua senha (a senha deve conter 4 números EX: 1234: )")
            if not cls.checar_senha_adm(cls, senha):
                print('Digite sua senha corretamente!')
                time.sleep(1)
                continue
            while True:
                if cls.validar_email(cls, email_checagem):
                    print("Esse email já está cadastrado, digite o email correto")
                    #adicionar função para levar para o login caso queira
                    continue
                break
            print("Vai ser gerado um código aleatório de segurança\nNÃO O PERCA! ELE SERÁ UTILIZADO CASO ESQUEÇA A SENHA")
            codigo = randint(1000, 9999)
            print(f'Seu código : {codigo}')
            time.sleep(1)
            try:
                cursor.execute("INSERT INTO adm_nova (email, senha, codigo) VALUES (%s, %s, %s)", (email_checagem, senha, codigo))
                conexao.commit()
            except Exception as e : 
                print (f"Houve um erro, por favor reporte aos administradores do programa\nCódigo do erro: {type(e).__name__}")
                time.sleep(1) #type(e).__name__
                cls.cadastro_adm()

            cls.email = email_checagem
            cls.senha = senha
            cls.codigo = codigo
            senha_check = False
            print("Parabéns, você agora está cadastrado no sistema\n" \
            "Você será redirecionado à página de  login")
            cls.login_adm()
    @classmethod
    def login_adm(cls):
        print("Você está no login!")
        email = True
        while email:
            email_checagem = input("Qual é o seu email ?")
            if not cls.validar_modelo_email(email_checagem):
                print("Digite seu email corretamente")
                continue

            while True:
                senha_digitada = input('Digite sua senha: ')
                if not cls.checar_senha_adm(cls, senha_digitada):
                    print('Digite sua senha corretamente!')
                    continue
                cursor.execute(f"SELECT senha FROM adm_nova WHERE email = %s", (email_checagem,))
                senha_banco = cursor.fetchone()
                senha_banco = senha_banco[0] if senha_banco else None
                if not cls.validar_email(cls, email_checagem) or senha_digitada != str(senha_banco):
                    print("Seu email, senha ou ambos estão incorretos")
                    while True:
                        escolha = input("Se você deseja digitar novamente, digite 1\n" \
                        "Se você deseja ir para a página de cadastro, digite 2: ")
                        if escolha == 2: 
                            print("Você irá para o cadastro")
                            cls.cadastro_adm()
                            break
                        if escolha == 1:
                            break
                    continue
                email = False
                break

            cursor.execute(f"SELECT codigo FROM adm_nova WHERE email = %s", (email_checagem,))
            codigo = cursor.fetchone()

            cls.email = email_checagem
            cls.senha = senha_banco
            cls.codigo = codigo

    def validar_modelo_email(email):
        try:
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)      

def adm():
    while True:
        escolha = input('Bem vindo administrador!\nO que você deseja fazer?\n1 - Cadastrar Usuário\n2 - Login\nEscolha entre as opções disponíveis: ')
        if escolha == '1':
            print('Você está sendo redirecionado para o cadastro!')
            time.sleep(1)
            admin_cadastrado = Admin.cadastro_adm() # Pass conexao and cursor
            break
        elif escolha == '2':
            print('Você está sendo redirecionado para o login!')
            time.sleep(1)
            admin_logado = Admin.login_adm() # Pass conexao and cursor
            break
        else:
            print('Digite uma opção válida!')
            time.sleep(1)
            continue



