from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras
import time,re
import sys

parser = reqparse.RequestParser()
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
parser.add_argument('name', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('date_of_birth', type=str)
parser.add_argument('self_description', type=str)
parser.add_argument('photo', type=str)
parser.add_argument('token', type=str)
parser.add_argument('phone', type=str)


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
        error = None
        token = None
        photo = None
        unread_message = None
        unread_trip = None
        verified = None
        user_id = None
        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        
        cursor.execute("select password,verified,id,unread_message,unread_trip from user_information where email = '{}';".format(email))
        results = cursor.fetchall()

        if len(results) != 0:
            user = results[0]
            if password == user['password']:
                token = "id" +str(user['id'])+"_"+ str(int(time.time()))
                verified = user['verified']
                user_id = user['id']
                unread_message = user['unread_message']
                unread_trip = user['unread_trip']
                cursor.execute("select position from user_photo where user_id = '{}';".format(user['id']))
                results = cursor.fetchall()
                if len(results) != 0:
                    photo = results[0]['position']
                else:
                    photo = None
            else:
                error = 'incorrect password'
        else:
            error = 'no such user'
        
        close_db(conn)
        if error == None:
            return {"reason" : error,
                    "user_id": user_id,
                    "photo" : photo,
                    'unread_message':unread_message,
                    'unread_trip':unread_trip,
                    "token" : token ,
                    "verified" : verified},200
        else:
            return {"reason" : error,
                    "user_id": user_id,
                    "photo" : photo,
                    'unread_message':unread_message,
                    'unread_trip':unread_trip,
                    "token" : token ,
                    "verified" : verified},400
            
class Register(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
        name = args['name']
        gender = args['gender']
        birthday = args['date_of_birth']
        description = args['self_description']
        photo = args['photo']
        phone = args['phone']
        error = None
        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        if email == None:
            error = 'Email is required.'
        elif password == None:
            error = 'Password is required.'
        elif name == None:
            error = 'Username is required.'
        elif not gender in ('F','M'):
            error = 'Gender should be F or M'
        if error != None:
            return {'reason':error},400
        cursor.execute("select * from user_information where email='{}';".format(email))
        results = cursor.fetchall()
        if len(results) != 0:
            error= 'User already exists.\nCreate user with another email.'
            return {'reason':error},403

        current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute("insert into user_information \
(email,password,name,gender,date_of_birth,self_description,create_date,unread_message,unread_trip,verified,phone)\
values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(email,password,name,gender,birthday,description,current_date,0,0,False,phone))
        conn.commit()

        if not photo:
            photo = "https://a0.muscache.com/im/pictures/20180027/bb9ccce5_original.jpg?aki_policy=large"
        cursor.execute("select id from user_information where email='{}';".format(email))
        results = cursor.fetchall()
        user_ID = results[0]['id']
        
        cursor.execute("insert into user_photo (user_id,position) values('{}','{}');".format(user_ID,photo))
        conn.commit()
        close_db(conn)
        return {'reason':error},200
    
class Edit_profile(Resource):
    def get(self):
        args = parser.parse_args()
        token = args['token']
        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        timepoint = float(re.sub(r'.*_','',token))
        userID = int(re.search(r"id(\d+)_",token).group(1))
        if time.time()-timepoint > 600:
            error = "Request timeout."
            return {"name" : None,
                "gender" : None,
                "phone" : None,
                "date_of_birth" : None,
                "self_description" : None,
                "photo" : None,
                "reason" : error},400
        cursor.execute("select id,name,gender,phone,date_of_birth,self_description from user_information where id = '{}';".format(userID))
        results = cursor.fetchall()
        user_info = results[0]
        cursor.execute("select position from user_photo where user_id='{}';".format(user_info['id']))
        results = cursor.fetchall()
        user_info.pop('id')
        user_info['date_of_birth']=str(user_info['date_of_birth'])
        user_info['photo'] = results[0]['position']
        user_info['reason'] = None
        close_db(conn)
        return user_info,200
    
    def put(self):
        args = parser.parse_args()
        token = args['token']
        name = args['name']
        gender = args['gender']
        phone = args['phone']
        birthday = args['date_of_birth']
        description = args['self_description']
        photo = args['photo']
        error = None

        timepoint = float(re.sub(r'.*_','',token))
        userID = int(re.search(r"id(\d+)_",token).group(1))
        if time.time()-timepoint > 600:
            error = "Request timeout."
            return {'reason':error},400
        
        if name == None:
            error = 'Username is required.'
            return {'reason':error},404
        elif not gender in ('F','M'):
            error = 'Incorrect gender type.'
            return {'reason':error},404

        cursor, conn = connect_db()
        cursor.execute("update user_information set name='{}', gender='{}', phone='{}',\
date_of_birth='{}',self_description='{}' where id='{}';".format(name,gender,phone,birthday,description,userID))
        conn.commit()
        cursor.execute("update user_photo set position='{}' where user_id='{}';".format(photo,userID))
        conn.commit()
        close_db(conn)
        return {'reason':error},200
        
class Logout(Resource):
    pass


