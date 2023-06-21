from flask import Flask # from f:소문자, import F:대문자
from flask_restful import Api # A 구분
from config import Config
from resources.user import UserRegisterResource 


app= Flask(__name__) # 여기도 F:대문자
print('app 변수 생성') # 디버깅용

# 환경변수 세팅
app.config.from_object(Config)

api = Api(app) # api 변수에 Flask를 넣음

# 경로(URL의 path:포트뒤/path/쿼리앞)와 API동작코드(Resource)를 연결한다.
api.add_resource(UserRegisterResource, '/user/register') # 회원가입


if __name__== '__main__':
    app.run()