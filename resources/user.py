from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError # emaill 체크
from utils import check_password, hash_password # 비밀번호 암호화
from flask_jwt_extended import create_access_token, get_jwt, jwt_required # login 연장기능 섞여있음
import datetime


### 회원가입
class UserRegisterResource(Resource):
    
    def post(self):
        #  {"email": "aaa@naver.com", 
        #   "password": "1234",
        #   "nickname": "홍길동" } # body- json을 보면서 하려고 작성해둠
    
        # 1. 클라이언트가 보낸 데이터를 받아준다.(body : JSON)
        data = request.get_json() # 이 데이터가 username, email, password
        print(data) # 디버깅용
        
        # 2. 이메일 주소형식이 올바른지 확인한다.(가입 정보를 잘 기입했는지 체크)
        # $pip install email-validator
        try:
            validate_email(data['email']) # email 체크
        except EmailNotValidError as e:
            return {"result":"fail", "error": str(e)}, 400 # 상태코드 응답
        
        # 3. 비밀번호 길이가 유효한지 체크한다.
        # 만약, 비번이 4자리 이상, 12자리 이하라고 한다면        
        if len(data['password'])<4 or len(data['password']) >12:
            return {"result":"fail", "error": '비번 길이 에러'}, 400 
            
        # 4. 비밀번호를 암호화 한다.
        # $pip install psycopg2-binary, $pip install passlib
        hashed_password= hash_password(data['password'])
        print(str(hashed_password))
        
        # 5. DB에 이미 있는지 확인한다.
        try:
            connection= get_connection()
            query= '''select * from user
                        where email = %s;'''
            record= (data['email'],)
            
            cursor= connection.cursor(dictionary=True)
            cursor.execute(query, record)
            
            result_list= cursor.fetchall()
            print(result_list)
            
            if len(result_list)==1:
                return {'result':'fail', 'error':'이미 회원가입 한 사람'}, 400
            
            # 회원이 아니므로, 회원가입 코드를 작성한다.
            query= '''insert into user
                        (email, password, nickname)
                    values
                        (%s, %s, %s);'''
            record= (data['email'],
                     hashed_password,
                     data['nickname']) # password는 유저가 보낸거X 암호화한 것으로
            cursor= connection.cursor()
            cursor.execute(query, record)
            
            connection.commit() # DB에 적용하라.
            
            ### DB에 데이터를 insert 한 후에 insert된 행의 ID를 가져오는 코드!!
            user_id= cursor.lastrowid # id값이 증가(AI)된 것을 가져와라..?
            
            cursor.close()
            connection.close()
            
            
        except Error as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 500 # 500: DB Error
    
        # create_access_token(user_id, expires_delta=datetime.timedelta(days=10)) # 로그인 연장
        access_token= create_access_token(user_id)
        
        return {'result': 'success', 'access_token' : access_token}


### 로그인 관련 개발
class UserLoginResource(Resource):
    def post(self) :
    # {
    # "email": "aaa@naver.com", 
    # "password": "1234"
    # } # body- json을 보기위해 작성해둠
        
        # 1. 클라이언트로부터 데이터를 받아온다.
        data= request.get_json()
        
        # 2. 이메일 주소로 DB에 Select 한다.
        try:
            connection= get_connection()
            query= '''select * from user
                    where email = %s;'''
            record= (data['email'],)            
            cursor= connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list= cursor.fetchall()
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 500
        # email 조사한다.
        if len(result_list)==0:
                return {'result':'fail', 'error':'회원가입한 사람 아님.'}, 400
            
        # 3. 비밀번호가 일치하는지 확인한다.
        # 암호화 시키고, 암호화된 비밀번호가 일치 확인
        print(result_list)
        # 비밀번호 비교?
        check= check_password(data['password'], result_list[0]['password'])
            # 일치하는지 확인할 때, 사용하면 안되는 쿼리문?
            # select * from user where email= 'abc@naver.com and password= 'gdgd';
      
        if check==False: # 비번이 틀렸으면?
            return {'result':'Fail', "Error":"비번 틀렸음"},400
        
        # 4. 클라이언트에게 데이터를 보내준다. (유저 아이디도 보내준다.)
        # 'user_id': result_list[0]['id']를 JWT로 암호화 해서!
        access_token = create_access_token(result_list[0]['id']) # 암호화
        return {'result':'success', 'access_token': access_token }
    

### 로그아웃
# 로그아웃된 토큰을 저장할 set을 만든다.
jwt_blocklist= set()
class UserLogoutResource(Resource):
    @jwt_required() # 블락 리스트에 넣어..야.. 뭐라뭐라 암튼 필수
    def delete(self):
        jti= get_jwt()['jti']
        print(jti)
        jwt_blocklist.add(jti)
        
        return{'result' : 'success'}


