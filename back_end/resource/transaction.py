from flask_restful import Resource, reqparse
from common.db_init import connect_db, close_db
from common.parser import token_parser
import psycopg2.extras
import sys,datetime,time

parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('host_id', type=int)
parser.add_argument('user_id', type=int)
parser.add_argument('transaction_id', type=int)
parser.add_argument('status', type=str)

class Confirm_Host(Resource):
    def post(self):
        args = parser.parse_args()
        token = args['token']
        host = args['host_id']
        transaction = args['transaction_id']
        status = args['status']
        error = None

        userID, timepoint = token_parser(token)
        if time.time() - timepoint > 600:
            error = 'Request timeout.'
        elif host == None:
            error = 'Host id required.'
        elif host != userID:
            error = 'Request rejected.'
        elif transaction == None:
            error = 'Transaction id required.'
        elif status == None or not status in ('accept','decline'):
            error = 'Invalid status required.'
        if error != None:
            return {'reason': error},400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        if status == 'accept':
            status_code = 'A'
            cursor.execute("select start_date,end_date,item_id from transaction where id={};".format(transaction))
            results = cursor.fetchall()
            start = results[0]['start_date']
            end = results[0]['end_date']
            date = start
            item = results[0]['item_id']
            while date <= end:
                cursor.execute("insert into unavailable_date (item_id,date) values({},'{}')".format(item,date))
                conn.commit()
                date += datetime.timedelta(1)
        elif status == 'decline':
            status_code = 'U'
        cursor.execute("update transaction set status='{}' where id={};".format(status_code,transaction))
        conn.commit()
        cursor.execute("select user_id from transaction where id={};".format(transaction))
        user = cursor.fetchall()[0]['user_id']
        cursor.execute("update user_information set unread_trip = unread_trip+1 where id = {};".format(user))
        conn.commit()
        close_db(conn)

        return {'reason': error},200

class Confirm_User(Resource):
    def post(self):
        args = parser.parse_args()
        token = args['token']
        user = args['user_id']
        transaction = args['transaction_id']
        status = args['status']
        error = None

        userID, timepoint = token_parser(token)
        if time.time() - timepoint > 600:
            error = 'Request timeout.'
        elif user == None:
            error = 'User id required.'
        elif user != userID:
            error = 'Request rejected.'
        elif transaction == None:
            error = 'Transaction id required.'
        elif status == None or status != 'cancel':
            error = 'Invalid status required.'
        if error != None:
            return {'reason': error},400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("select status from transaction where id={};".format(transaction))
        origin_status = cursor.fetchall()[0]['status']
        if origin_status == 'S':
            error = 'Transaction already completed.'
            return {'reason': error},400
        elif origin_status == 'U':
            error = 'Transaction already declined.'
            return {'reason': error},400
        elif origin_status == 'A':
            cursor.execute("select start_date,end_date,item_id from transaction where id={};".format(transaction))
            results = cursor.fetchall()
            start = results[0]['start_date']
            end = results[0]['end_date']
            date = start
            item = results[0]['item_id']
            while date <= end:
                cursor.execute("delete from unavailable_date where item_id={} and date='{}';".format(item,date))
                conn.commit()
                date += datetime.timedelta(1)
        cursor.execute("update transaction set status='{}' where id={};".format('U',transaction))
        conn.commit()
        cursor.execute("select host_id from transaction where id={};".format(transaction))
        host = cursor.fetchall()[0]['host_id']
        cursor.execute("update user_information set unread_trip = unread_trip+1 where id = {};".format(host))
        conn.commit()
        close_db(conn)

        return {'reason': error},200
