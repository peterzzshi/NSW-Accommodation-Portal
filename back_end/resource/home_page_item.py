from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras

parser = reqparse.RequestParser()

parser.add_argument("page_number", type=int)
#
# house_list = []
class Home_page_item(Resource):
    def get(self):
        args = parser.parse_args()
        if not args['page_number']:
            return {"reason" : "no page number"}, 400
        # house_list = []
        # if not house_list:
        cursor, conn = connect_db()
        cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_dict.execute("""select name, id, accuracy, communication, cleanliness,
                                location, check_in, value, rating_number, price 
                                from item""")
        house_list = cursor_dict.fetchall()
        for row in house_list:
            if row['rating_number']:
                row['rating'] = (row.pop('accuracy') + row.pop('communication') + row.pop('cleanliness') + \
                                 row.pop('location') + row.pop('check_in') + row.pop('value')) / (
                                            6 * row['rating_number'])
            else:
                row['rating'] = (row.pop('accuracy') + row.pop('communication') + row.pop('cleanliness') + \
                                 row.pop('location') + row.pop('check_in') + row.pop('value'))
            row['price'] = float(row['price'])
            cursor.execute("""select position from item_photo where item_id = {}""".format(row['id']))
            image_result = cursor.fetchone()
            if image_result:
                row['image'] = cursor.fetchone()[0]
            else:
                row['image'] = ''

        if (args['page_number'] - 1) * 6 >= len(house_list) or args['page_number'] <= 0:
            return {"reason" : "incorrect page number"}, 400

        end_flag = min(args['page_number'] * 6, len(house_list))
        if args['page_number'] == 1:
            start_flag = 0
        else:
            start_flag = (args['page_number'] - 1) * 6

        dict_return = {}
        dict_return['items'] = house_list[start_flag:end_flag]
        if (args['page_number'] * 6) >= len(house_list):
            dict_return['exist_next_pages'] = 0
        else:
            dict_return['exist_next_pages'] = 1
        return dict_return, 200
