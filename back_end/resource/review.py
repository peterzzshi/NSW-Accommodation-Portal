from flask_restful import Resource, reqparse
from common.db_init import connect_db, close_db
from common.parser import token_parser
import psycopg2.extras
import sys,datetime,time

parser = reqparse.RequestParser()
parser.add_argument('item_id', type=int)
parser.add_argument('token', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('transaction_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('comment', type=str)
parser.add_argument('accuracy', type=int)
parser.add_argument('communication', type=int)
parser.add_argument('cleanliness', type=int)
parser.add_argument('location', type=int)
parser.add_argument('check_in', type=int)
parser.add_argument('value', type=int)

class Review(Resource):
    def get(self):
        args = parser.parse_args()
        item = args['item_id']
        error = None

        if item == None:
            error = 'Item ID required.'
            return {'review':[],
                    'result':error},400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute("select * from item_comment where item_id={};".format(item))
        reviews = cursor.fetchall()
        for r in reviews:
            cursor.execute("select position from user_photo where user_id={};".format(r['user_id']))
            results = cursor.fetchall()
            if len(results)==0:
                r['user_photo'] = None
            else:
                r['user_photo'] = results[0]['position']
            r['date'] = str(r['date'])
            r.pop('id')
            r.pop('item_id') 
        close_db(conn)
        return {'review':reviews,
                'result':error},200

    def post(self):
        args = parser.parse_args()
        token = args['token']
        user = args['user_id']
        transaction = args['transaction_id']
        date = args['date']
        comment = args['comment']
        accuracy = args['accuracy']
        communication = args['communication']
        cleanliness = args['cleanliness']
        location = args['location']
        checkin = args['check_in']
        value = args['value']
        error = None

        userID, timepoint = token_parser(token)
        if time.time() - timepoint > 600:
            error = 'Request timeout.'
        elif user == None:
            error = 'User ID required.'
        elif user != userID:
            error = 'Request rejected.'
        elif transaction == None:
            error = 'Transaction required.'
        if error != None:
            return {'result': error},400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("select item_id from transaction where id={} and status='{}';".format(transaction,'S'))
        results = cursor.fetchall()
        if len(results)==0:
            error = "Transaction is not existing or not completed."
            return {'result': error},400
        cursor.execute("update transaction set rating_or_not=true where id={} and status='{}';".format(transaction,'S'))
        conn.commit()
        item = results[0]['item_id']
        cursor.execute("insert into item_comment (user_id,item_id,date,comment,accuracy,communication,cleanliness,location,check_in,value) values({},{},'{}','{}','{}','{}','{}','{}','{}','{}');".format(user,item,date,comment,accuracy,communication,cleanliness,location,checkin,value))
        conn.commit()
        close_db(conn)
        return {'reason':error},200
