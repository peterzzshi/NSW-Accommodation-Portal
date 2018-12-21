from flask_restful import Resource, reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras
import re,sys,time

parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('item_id', type=int)
parser.add_argument('user_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('comment', type=str)


class Book(Resource):
    def post(self):
        args = parser.parse_args()
        token = args['token']
        item = args['item_id']
        user = args['user_id']
        date = args['date']
        start = args['start_date']
        end = args['end_date']
        comment = args['comment']
        error = None

        user_check = int(re.search(r"id(\d+)_", token).group(1))
        timepoint = float(re.sub(r'.*_', '', token))
        if time.time() - timepoint > 600:
            error = 'Request timeout'
        elif user != user_check:
            error = 'Request rejected'
        elif item == None:
            error = 'Item required.'
        elif user == None:
            error = 'User required.'
        elif start == None:
            error = 'Start date required.'
        elif end == None:
            error = 'End date required.'
        elif start>end:
            error = 'Incorrect date period input.'
        if error != None:
            return {'reason': error}, 400

        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute("select hoster_id from item where id={};".format(item))
        host = cursor.fetchall()[0]['hoster_id']
        cursor.execute("insert into transaction (item_id,user_id,host_id,status,date,start_date,end_date,rating_or_not,comment) values ({},{},{},'{}','{}','{}','{}',{},'{}');".format(item,user,host,'P',date,start,end,False,comment))
        conn.commit()
        cursor.execute("update user_information set unread_trip=unread_trip+1 where id={};".format(host))
        conn.commit()
        close_db(conn)
        return {'reason': error}, 200
