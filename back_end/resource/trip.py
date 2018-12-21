from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras
import re,datetime,time
import sys

parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('user_id', type=int)

class Trip(Resource):
    def get(self):
        args = parser.parse_args()
        token = args['token']
        user = args['user_id']
        error = None
        
        timepoint = float(re.sub(r'.*_','',token))
        user_check = int(re.search(r"id(\d+)_",token).group(1))
        if time.time()-timepoint > 600 :
            error = 'Request timeout.'
        elif user==None:
            error = 'User required.'
        elif user != user_check:
            error = 'Request rejected.'
        if error != None:
            return {'transaction':[],
                    'reason': error},400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("select id,item_id,user_id,host_id,status,start_date,end_date,rating_or_not from transaction where user_id = {} or host_id={};".format(user,user))
        trips = cursor.fetchall()
        
        current_date = datetime.date.today()

        for t in trips:
            if t['user_id'] == user:
                cursor.execute("select name from user_information where id={};".format(t['host_id']))
                user_name = cursor.fetchall()[0]['name']
                cursor.execute("select position from user_photo where user_id={};".format(t['host_id']))
                results = cursor.fetchall()
                if len(results)==0:
                    user_photo = None
                else:
                    user_photo = results[0]['position']
                t['trip_or_not'] = True
                t['user_id']=t['host_id']
            else:
                cursor.execute("select name from user_information where id={};".format(t['user_id']))
                user_name = cursor.fetchall()[0]['name']
                cursor.execute("select position from user_photo where user_id={};".format(t['user_id']))
                results = cursor.fetchall()
                if len(results)==0:
                    user_photo = None
                else:
                    user_photo = results[0]['position']
                t['trip_or_not'] = False
            t['user_name'] = user_name
            t['user_photo'] = user_photo
            cursor.execute("select name from item where id={};".format(t['item_id']))
            item_name = cursor.fetchall()[0]['name']
            t['house_name'] = item_name
            t['transaction_id'] = t['id']
            t['house_id'] = t['item_id']
            t['review_or_not'] = t['rating_or_not']
            if t['status'] == 'A':
                if current_date > t['end_date']:
                    cursor.execute("update transaction set status='{}' where id={};".format('S',t['id']))
                    conn.commit()
                    t['status'] = 'completed'
                else:
                    t['status'] = 'accepted'
            elif t['status'] == 'U':
                t['status'] = 'declined'
            elif t['status'] == 'P':
                t['status'] = 'pending'
            elif t['status'] == 'S':
                t['status'] = 'completed'
            t['start_date'] = str(t['start_date'])
            t['end_date'] = str(t['end_date'])
            t.pop('id')
            t.pop('item_id')
            t.pop('host_id')
            t.pop('rating_or_not')

        cursor.execute("update user_information set unread_trip=0 where id ={};".format(user))
        conn.commit()
        close_db(conn)       
        return {'transaction': trips,
                'reason': error},200
                
