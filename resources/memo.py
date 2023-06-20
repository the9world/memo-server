from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection

# Resource : 데이터의 코드 만드는 Class

# API 동작하는 코드를 만들기 위해서는 class(클래스)를 만들어야 한다.

# class 란? 비슷한 데이터끼리 모아놓은 것 (Table을 생각) : class는 상속이 가능.
# class는 변수와 함수로 구성된 묶음
# Table과 다른 점; : 함수가 있다는 점

# API를 만들기 위한 class는
# flask_restful 라이브러리의 Resource class를 상속해서 생성.


class FollowMemoListResource(Resource):
    @jwt_required()
    def get(self):
        # 1. 클라이언트로부터 데이터를 받아온다.(body는 request.get_json())
        # query params는 딕셔너리로 받아오고,
        # 없는 키값을 억세스해도 에러 발생하지 않도록 (없는 값 None)
        # 딕셔너리의 get 함수를 사용해서 데이터를 받아온다.
        offset= request.args.get('offset')
        limit = request.args.get('limit')
        
        user_id= get_jwt_identity()
        
        try:
            connection= get_connection()
            query= '''select m.*, u.nickname
                    from follow f
                    join memo m
                        on f.followeeId= m.userId
                    join user u
                        on m.userId = u.id
                    where f.followerId= %s
                    order by date desc
                    limit '''+offset+''', '''+limit+''';'''
            # offset, limit 사용법 '''+변수+''', '''+변수+'''  ;'''

            record = (user_id, ) # 변수 뒤에 ","는 1개의 변수라도 튜플로 하기 위해.
            print(record)
            cursor = connection.cursor(dictionary=True) # 클라이언트에게 반환해서 돌려줘야할 때
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}, 500

        
        i = 0
        for row in result_list : # result_list에서 행을 하나씩 가져온다
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            result_list[i]['date'] = row['date'].isoformat()
            i = i + 1
        
        return {'result' : 'success', 'count':len(result_list), 'item' : result_list}


class MemoResource(Resource): # 메모 수정
    @jwt_required()
    def put(self, memo_id):
        data= request.get_json()
        
        # header에 담긴 JWT 토큰을 받아온다.(user_id 받아온다)
        user_id= get_jwt_identity()
        try:
            connection= get_connection()
            query= '''update memo
                set title = %s, date= %s, content= %s
                    where id =%s and userId= %s;'''
            record= (data['title'], data['date'],
                     data['content'], memo_id, user_id) 
            print(record)
            cursor= connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e :
            print(e)
            return{"result":"fail", "error": str(e)},500
        
        return {"result":"success"}
    
    
    @jwt_required()
    def delete(self, memo_id):
        # 1. 클라이언트로부터 데이터를 받아온다.
        print(memo_id)
        # 1-1. header에 담긴 JWT 토큰을 받아온다.(user_id 받아온다)
        user_id= get_jwt_identity()
        # 2. DB에서 삭제한다.
        try:
            connection= get_connection()
            query= '''delete from memo
                        where id= %s and userId= %s;'''
            record= (memo_id, user_id)
            cursor= connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {"result": "fail", "error": str(e)}
        # 3. 결과를 응답한다.
        
        return {"result":"succes"}


class MemoListResource(Resource): # 메모 등록
    @jwt_required()
    def post(self) : # class 안의 def 함수 입력 값은 self
        # PostMan(클라이언트)에서 POST 요청을 받아서 해당 POST 함수를 실행
        # { "title":"무언가"
        #   "date":"언젠가"
        #   "content": "무엇이든"}
         # 1. 클라이언트가 보낸 데이터를 받아온다. (유저의 요청을 받음)
        data = request.get_json()
        
        # 1-1. header에 담긴 JWT 토큰을 받아온다.
        user_id= get_jwt_identity()
        
        # 2. DB에 저장한다.
        try :
            # 2-1. 데이터베이스를 연결한다. 
            connection = get_connection()

            # 2-2. 쿼리문을 만든다.
# # # # 칼럼과 매칭되는 데이터만 %s(포맷팅: 유저입력)로 바꿔준다. # # # # 
            query = '''insert into memo
                    (title, date, content, userId)
                        values
                    (%s, %s, %s, %s);'''
                    
            # 2-3. 쿼리에 매칭되는 변수 처리 ★중요★ 튜플로 처리한다.
            record = ( data['title'], data['date'],
                        data['content'], user_id)
            
            # 2-4. 커서를 가져온다.
            cursor= connection.cursor()
            
            # 2-5. 쿼리문을 실행한다.
            cursor.execute(query, record)
            
            # 2-6. DB에 반영 완료하라는 commit 해줘야 한다.
            connection.commit()
            
            # 2-7. 자원해제
            cursor.close()
            connection.close()
            
        except Error as e :  # Erorr는 mysql 라이브러리
            print(e)
            return {'result' : 'fail', 'error' : str(e) }, 500
        
        # 3. 에러가 났으면, 에러 라고 알려주고, 아니면 잘 저장되었다고 알려준다.

        # 응답할 땐(return) JSON으로 작성 
        return {"result" : "success"}
    
    
    @jwt_required()
    def get(self):
        # 1-1. header에 담긴 JWT 토큰을 받아온다.
        user_id= get_jwt_identity()
        
        # 2-1. DB 커넥션
        try:
            connection= get_connection()

        # 2-2. 쿼리문 만든다.
            query='''select *
                    from memo
                    where userId = %s
                    order by date desc;'''
                    
            record = (user_id,)
            
            # 2-4. 커서 가져온다.
            cursor = connection.cursor(dictionary= True) # dic파라미터:True:json 반환
            # 2-5. 쿼리문을 실행한다.
            cursor.execute(query, record)
            # 2-6. 실행 결과를 가져온다.
            result_list= cursor.fetchall()

            # 2-7. 자원해제
            cursor.close()
            connection.close()
            
        except Error as e :
            print(e)
            return {'result': 'fail', 'error': str(e) } , 500
        
            # 3. 데이터가공이 필요하면 가공 후 클라이언트에 응답한다.
        i = 0
        for row in result_list : # [DB 칼럼이름]
            result_list[i]['date']= row['date'].isoformat() # DateType->문자열 변환
            result_list[i]['createdAt']= row['createdAt'].isoformat() # DateType->문자열 변환
            result_list[i]['updatedAt']= row['updatedAt'].isoformat() # DateType->문자열 변환
            i = i + 1
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list} # 200=정상=작성NO, 그 외는 상태코드 리턴