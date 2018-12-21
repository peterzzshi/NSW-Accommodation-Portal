from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
from common.parser import token_parser
import psycopg2.extras

parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('user_id', type=int)

cursor, conn = connect_db()

class Post_specific(Resource):
    def get(self):
        args = parser.parse_args()
        toke = args['token']
        user = args['user_id']

        if not user:
            return {"reason" : "no user id"}, 400

        ## need to check token

        cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_dict.execute("""select * from post where user_id = {}""".format(user))
        rows = cursor_dict.fetchall()
        rows.sort(key=lambda x: x['id'], reverse=True)
        for i in rows:
            i['start_date'] = i['start_date'].strftime("%Y-%m-%d")
            i['end_date'] = i['end_date'].strftime("%Y-%m-%d")
            i['post_date'] = i['post_date'].strftime("%Y-%m-%d")
            i['post_id'] = i.pop('id')
        dict_return = {}
        dict_return['Post'] = rows
        dict_return['reason'] = ""
        return dict_return, 200