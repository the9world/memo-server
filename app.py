from flask import Flask # from f:소문자, import F:대문자
from flask_restful import Api # A 구분
from config import Config 
from flask_jwt_extended import JWTManager

from resources.follow import FollowResource
from resources.memo import FollowMemoListResource, MemoListResource, MemoResource
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource, jwt_blocklist

app= Flask(__name__) # 여기도 F:대문자
print('app 변수 생성') # 디버깅용

# 환경변수 세팅
app.config.from_object(Config) # config.py class config 상속(?)받음

        # JWT 매니저 초기화
# Flask-JWT-Extended 확장에 대한
# JWT 설정 및 콜백 기능을 보유하는 데 사용되는 개체..?
jwt= JWTManager(app)
print('jwt 매니저 초기화') # 디버깅용

# 로그아웃된 토큰으로 요청하는 경우!  이 경우는 비정상적인 경우 이므로
# jwt가 알아서 처리하도록 코드작성 (함수는 정해져있다)
@jwt.token_in_blocklist_loader # 유효하지 않은 블락리스트에 있는 토큰 관리하겠다.
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app) # api 변수에 Flask를 넣음

# 경로(URL의 path:포트뒤/path/쿼리앞)와 API동작코드(Resource)를 연결한다.
api.add_resource(UserRegisterResource, '/user/register') # 회원가입
api.add_resource(UserLoginResource, '/user/login') # 로그인
api.add_resource(UserLogoutResource, '/user/logout') # 로그아웃
api.add_resource(MemoListResource, '/memo') # 메모 등록
api.add_resource(MemoResource, '/memo/<int:memo_id>') # 메모 수정 <int:memo_id> 인트인 메모아이디를 입력받음
api.add_resource(FollowResource, '/follow/<int:followee_id>') # 친구 맺기 상대 weeId : 나는 werID
api.add_resource(FollowMemoListResource, '/follow/memo')

if __name__== '__main__':
    app.run()
    
