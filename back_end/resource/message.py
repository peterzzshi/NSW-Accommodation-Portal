from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras
import re,time
import sys

parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('sender_id', type=int)
parser.add_argument('receiver_id', type=int)
parser.add_argument('message_content', type=str)
parser.add_argument('date', type=str)

class Message(Resource):
    def get(self,request):
        if request == 'detail':
            args = parser.parse_args()
            token = args['token']
            user1_ID = args['user_id']
            user2_ID = args['receiver_id']
            error = None

            userID = int(re.search(r"id(\d+)_",token).group(1))
            timepoint = float(re.sub(r'.*_','',token))
            if time.time()-timepoint > 600 or user1_ID != userID:
                return {'message':None, 'sender':None, 'receiver':None},400

            cursor, conn = connect_db()
            cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            
            cursor.execute("select id,name from user_information where id='{}';".format(user1_ID))
            results = cursor.fetchall()
            if len(results) == 0:
                return {'message':None, 'sender':None, 'receiver':None},400
            user1 = results[0]
            cursor.execute("select position from user_photo where user_id='{}';".format(user1_ID))
            results = cursor.fetchall()
            if len(results) == 0:
                user1['photo'] = None
            else:
                user1['photo'] = results[0]['position']
                
            cursor.execute("select id,name from user_information where id='{}';".format(user2_ID))
            results = cursor.fetchall()
            if len(results) == 0:
                return {'message':None, 'sender':None, 'receiver':None},400
            user2 = results[0]
            cursor.execute("select position from user_photo where user_id='{}';".format(user2_ID))
            results = cursor.fetchall()
            if len(results) == 0:
                user2['photo'] = None
            else:
                user2['photo'] = results[0]['position']
            
            cursor.execute("select content,sender,date from message where sender='{}' and receiver='{}' or sender='{}' and receiver='{}';".format(user1_ID,user2_ID,user2_ID,user1_ID))
            results = cursor.fetchall()
            message = sorted(results,key=lambda message:message["date"],reverse=True)
            for m in message:
                m['date'] = str(m['date'])
            cursor.execute("select count(*) as nums from message where sender='{}' and receiver='{}' and read_or_not = '{}';".format(user2_ID,user1_ID,False))
            results = cursor.fetchall()
            count = results[0]['nums']
            cursor.execute("update message set read_or_not=True where sender = '{}' and receiver = '{}' and read_or_not = '{}';".format(user2_ID,user1_ID,False))
            conn.commit()
            cursor.execute("update user_information set unread_message = unread_message-'{}' where id = '{}';".format(count,user1_ID))
            conn.commit()
            close_db(conn)
            
            return {'message':message, 'user':user1, 'sender':user2},200    
        elif request == 'preview':
            args = parser.parse_args()
            token = args['token']
            userID_check = args['user_id']
            error = None
            
            userID = int(re.search(r"id(\d+)_",token).group(1))
            timepoint = float(re.sub(r'.*_','',token))
            if time.time()-timepoint > 600 or userID_check != userID:
                return {'message':None},400
            
            cursor, conn = connect_db()
            cursor.execute("select * from message where sender = '{}' or receiver = '{}';".format(userID,userID))
            results = cursor.fetchall()
            close_db(conn)
            
            messages_dict = {}
            for record in results:
                if record[1] == userID:
                    chat_with = record[2]
                else:
                    chat_with = record[1]
                if not chat_with in messages_dict.keys():
                    messages_dict[chat_with] = record
                elif str(record[4]) > str(messages_dict[chat_with][4]):
                    messages_dict[chat_with] = record   
            messages_list=[]
            message={}
            for m in messages_dict.values():
                message['last_message'] = m[3]
                message['user_id'] = userID
                message['receiver_id'] = m[2]
                message['sender_id'] = m[1]
                message['read_or_not'] = m[6]
                messages_list.append(message)
                message ={}
            return {'message' :messages_list},200
    
    def post(self,request):
        args = parser.parse_args()
        token = args['token']
        sender = args['sender_id']
        receiver = args['receiver_id']
        content = args['message_content']
        date = args['date']
        error = None

        timepoint = float(re.sub(r'.*_','',token))
        userID = int(re.search(r"id(\d+)_",token).group(1))
        if time.time()-timepoint > 600 :
            error = "Request timeout."
            return {'reason': error},400
        if userID != sender:
            error = "Request rejected."
            return {'reason': error},400

        cursor, conn = connect_db()
        cursor.execute("insert into message (sender,receiver,content,date,read_or_not) values ('{}','{}','{}','{}','{}');".format(sender,receiver,content,date,False))
        conn.commit()
        close_db(conn)
        return {'reason': error},200
