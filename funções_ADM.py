import mysql.connector
import time
from random import randint
import funcoes_fastake as fk
from email_validator import EmailNotValidError, validate_email


class Adm:
    def __init__(self, email, senha, codigo):
        self.email = email
        self.senha = senha
        self.codigo = codigo

    def validar_email(self, email_checagem, conexao, cursor):
        cursor.execute(f"SELECT email FROM adm WHERE email = %s", (email_checagem,))
        resultado = cursor.fetchone()
        return bool(resultado)
        
    def checar_senha_adm(self, senha_checagem):
        while True:
            senha_checagem = input()
            if not senha_checagem.isdigit():
                print('Escreva apenas números, no formato (1234)')
                continue
            if not len(senha_checagem) == 4:
                print('Escreva exatamente 4 números, no formato (1234)')
                continue
            break
        return senha_checagem

    def cadastro_adm(self, conexao, cursor):
        while True:
            print('Vamos realizar seu cadastro!\nPor favor preencha os dados abaixo')
            email_checagem = input("Defina seu email: ")
            if not fk.validar_modelo_email(email_checagem):
                print("Digite seu email corretamente")
                continue
            break
        print("Defina sua senha (a senha deve conter 4 números EX: 1234: )")
        senha = self.checar_senha_adm()
        while True:
            if self.validar_email(email_checagem, conexao, cursor):
                print("Esse email já está cadastrado, digite o email correto")
                #adicionar função para levar para o login caso queira
                continue
            break
        print("Vai ser gerado um código aleatório de segurança\nNÃO O PERCA! ELE SERÁ UTILIZADO CASO ESQUEÇA A SENHA")
        codigo = randint(1000, 9999)

        try:
            cursor.execute("INSERT INTO adm (email, senha, codigo) VALUES (%s, %s, %s)", (email_checagem, senha, codigo))
            conexao.commit()
        except Exception as e : 
            print (f"Houve um erro, por favor reporte aos administradores do programa\nCódigo do erro: {type(e).__name__}")
            fk.inicio(conexao, cursor)

        self.email = email_checagem
        self.senha = senha
        self.codigo = codigo

        print("Parabéns, você agora está cadastrado no sistema\n" \
        "Você será redirecionado à página de inicio para realizar seu login")
        fk.inicio(conexao, cursor)

    def login_adm(self, conexao, cursor):
        print("Você está no login!")
        while True:
            email_checagem = input("Qual é o seu email ?")
            if not fk.validar_modelo_email(email_checagem):
                print("Digite seu email corretamente")
                continue

            print("Digite sua senha")
            senha_digitada = self.checar_senha_adm()
            cursor.execute(f"SELECT senha FROM adm WHERE email = %s", (email_checagem,))
            senha_banco = cursor.fetchone()

            if not self.validar_email(email_checagem, conexao, cursor) or senha_digitada != senha_banco:
                print("Seu email, senha ou ambos estão incorretos")
                while True:
                    escolha = input("Se você deseja digitar novamente, digite 1\n" \
                    "Se você deseja ir para a página de cadastro: digite 2")
                    if escolha == 2: 
                        print("Você irá para o cadastro")
                        self.cadastro_adm(conexao, cursor)
                        break
                    if escolha==1:
                        break
                continue
            break

        cursor.execute(f"SELECT codigo FROM adm WHERE email = %s", (email_checagem,))
        codigo = cursor.fetchone()

        self.email == email_checagem
        self.senha == senha_banco
        self.codigo == codigo

            


