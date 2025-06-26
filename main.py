import mysql.connector
import time
import funcoes_fastake as fk

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'Fastake'
)
cursor = conexao.cursor()

fk.inicio(conexao, cursor) 

cursor.close()
conexao.close()
