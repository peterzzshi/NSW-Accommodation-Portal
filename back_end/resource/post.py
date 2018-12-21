from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
from common.parser import token_parser
import psycopg2.extras


parser = reqparse.RequestParser()
parser.add_argument('token', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('country', type=str)
parser.add_argument('city', type=str)
parser.add_argument('suburb', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('post_date', type=str)
parser.add_argument('token', type=str)
parser.add_argument('token', type=float)
parser.add_argument('price_start', type=float)
parser.add_argument('price_end', type=float)
parser.add_argument('people_number', type=int)
parser.add_argument('comment', type=str)
parser.add_argument('post_id', type=int)

cursor, conn = connect_db()

class Post(Resource):
    def post(self):
        args = parser.parse_args()
        token = args['token']
        user = args['user_id']
        country = args['country']
        city = args['city']
        suburb = args['suburb']
        s_date = args['start_date']
        e_date = args['end_date']
        p_date = args['post_date']
        price_low = args['price_start']
        price_high = args['price_end']
        people = args['people_number']
        comment =  args['comment']

        # need check tooken

        # userID, timepoint = token_parser(token)
        # if userID != user:
        #     return {"result" : "user_id is not same as token"}, 400


        if not user or not price_low or not price_high or not people:
            return {"result" : "not null argument is null"}, 400


        cursor.execute("""insert into post(user_id, country, city, suburb, start_date, end_date, price_start, price_end, people_number, comment, post_date) 
                          values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                       .format(user, country, city,suburb, s_date, e_date, price_low, price_high,people, comment, p_date))
        conn.commit()
        return {"reason" : ""}, 200


    def get(self):
    #     # cursor_dict =
    #     cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_dict.execute("""select * from post""")
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

    def delete(self):
        args = parser.parse_args()
        token = args['token']
        user_id = args['user_id']
        post_id = args['post_id']

        # need check token

        if not post_id:
            return {"reason" : "not null argument is null"}, 400

        try:
            cursor.execute("""delete from post where id = {}""".format(post_id))
            conn.commit()
        except:
            return {"reason" : "post_id does not exist"}, 400

        return {"reason" : ""}, 200

    def put(self):
        args = parser.parse_args()
        token = args['token']
        user = args['user_id']
        country = args['country']
        city = args['city']
        suburb = args['suburb']
        s_date = args['start_date']
        e_date = args['end_date']
        p_date = args['post_date']
        price_low = args['price_start']
        price_high = args['price_end']
        people = args['people_number']
        comment =  args['comment']
        post_id = args['post_id']

        # need check tooken

        # userID, timepoint = token_parser(token)
        # if userID != user:
        #     return {"result" : "user_id is not same as token"}, 400

        """UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03' """


        if not user or not price_low or not price_high or not people or not s_date\
                or not e_date or not p_date:
            return {"result" : "not null argument is null"}, 400

        if not post_id:
            return {"result" : "no post id"}, 400

        cursor.execute("""update post set country = '{}', city = '{}', suburb = '{}', start_date = '{}',
                        end_date = '{}', post_date = '{}', price_start = '{}', price_end = '{}', 
                        people_number = '{}', comment = '{}' where id = '{}'"""
                       .format(country, city, suburb, s_date, e_date, p_date, price_low, price_high,
                               people, comment, post_id))

        conn.commit()
        return {"reason" : ""}, 200
