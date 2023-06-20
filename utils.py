# 개발하면서 유용한 함수들을 utils 에 모아두고 사용한다.
from passlib.hash import pbkdf2_sha256 # 단방향 암호화 라이브러리
from config import Config

# 1. 원문 비밀번호를, 단방향으로 암호화 하는 함수
def hash_password(original_password):
    password = pbkdf2_sha256.hash(original_password + Config.SALT)
    # config.salt 변수는  config 파일에 seed, randomstate
    return password

# 2. 유저가 입력한 비밀번호가 맞는지 체크하는 함수
def check_password(oiginal_password, hashed_password):
    #original: 유저비밀번호(+암호화조건),  hashed: 암호화비밀번호
    check= pbkdf2_sha256.verify(oiginal_password+ Config.SALT,
                                hashed_password) # verity: 검증함수
    return check
    