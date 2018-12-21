from flask_restful import Resource,reqparse,request
from datetime import datetime
from common.db_init import connect_db, close_db
from common.util import change_list_to_set_format
import psycopg2.extras
import time, re, json


parser = reqparse.RequestParser()

parser.add_argument("user_id", type=int)
parser.add_argument("token", type=str)

cursor, conn = connect_db()

class User_posts(Resource):
    def get(self):
        args = parser.parse_args()
        if not args['user_id']:
            return {"reason" : "no user_id"}, 404

        cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_dict.execute("""select * from post where user_id = '{}'""".format(args['user_id']))

        rows = cursor_dict.fetchall()
        rows.sort(key=lambda x: x['id'], reverse=True)
        for i in rows:
            i['start_date'] = i['start_date'].strftime("%Y-%m-%d")
            i['end_date'] = i['end_date'].strftime("%Y-%m-%d")
            i['post_date'] = i['post_date'].strftime("%Y-%m-%d")
            i['post_id'] = i.pop('id')
            try:
                cursor.execute("""select name from user_information where id = {}""".format(i['user_id']))
                user_name = cursor.fetchall()
                i['user_name'] = user_name[0][0]
            except:
                return {"reason" : "server error, cannot find user id"}, 500

            try:
                cursor.execute("""select position from user_photo where user_id = {}""".format(i['user_id']))
                user_photo = cursor.fetchall()
                i['user_photo'] = user_photo[0][0]
            except:
                i['user_photo'] = None

        dict_return = {}
        dict_return['posts'] = rows
        dict_return['reason'] = ""
        return dict_return, 200
