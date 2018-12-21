from common import item_type_information
from flask_restful import Resource,reqparse,request
from datetime import datetime
from common.db_init import connect_db, close_db
from common.util import change_list_to_set_format
import psycopg2.extras
import time, re, json


parser = reqparse.RequestParser()

parser.add_argument("user_id", type=int)

cursor, conn = connect_db()

class User_information(Resource):
    def get(self):
        cursor_dict = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        args = parser.parse_args()
        if not args['user_id']:
            return {"reason" : "no user_id"}, 404


        try:
            cursor_dict.execute("""select name, gender, self_description from user_information where id = {}""".format(args['user_id']))
        except:
            return {"reason" : "user_id error"}, 400

        res = cursor_dict.fetchall()[0]

        try:
            cursor.execute("""select position from user_photo where user_id = {}""".format(args['user_id']))
        except:
            return {"reason" : "no user photo"}, 400

        res['user_photo'] = cursor.fetchone()[0]
        print(res)

        return res, 200



