from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection

class FollowResource(Resource):
    @jwt_required()
    def post(self, followee_id):
        user_id= get_jwt_identity()
        
        try :
            connection= get_connection()
            query= '''insert into follow
                        (followerId, followeeId)
                    values
                        (%s, %s);'''
            record= (user_id, followee_id)
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
    
    @jwt_required()
    def delete(self, followee_id):
        user_id= get_jwt_identity()
        
        try :
            connection= get_connection()
            query= '''delete from follow
                    where followerId= %s and followeeId = %s;'''
            record= (user_id, followee_id)
            cursor= connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {"result": "fail", "error": str(e)}

        return {"result":"succes"}