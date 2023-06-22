# 프라이빗으로 만들기: .gitignore- config.py 추가하면 이 파일은 빼고 git에 올라감.
class Config: # MySQL Connection 만들때 처럼 HostName 등을 입력한다.
# 변수 이름은 사용자가 정의한다.
    HOST = 'mydb.codwds0bctbl.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'memo_db2'
    DB_USER = 'memo_db_user2'
    DB_PASSWORD = '3885'

    # 비번 암호화 : seed, SALT, Randomstate
    SALT = "0417@hello~"
    
    # JWT 변수 세팅 (JWT_SECRET_KEY 다르면 안됨 변수명 고정)
    JWT_SECRET_KEY = 'hello~!by@'
    JWT_ACCESS_TOKEN_EXPIRES = False # True하면 설정시간 경과 후 로그아웃
    PROPAGATE_EXCEPTIONS = True