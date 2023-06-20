# mysql_connection.py는 DataBase 연결 전용 파일
import mysql.connector
from config import Config

def get_connection():
    # mysql.connector 라이브러리에서 이렇게 사용하라고 되어있음.
    connection= mysql.connector.connect(
        host= Config.HOST,
        database= Config.DATABASE,
        user= Config.DB_USER,
        password= Config.DB_PASSWORD
    )
    
    return connection