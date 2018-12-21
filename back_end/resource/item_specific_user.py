from common import item_type_information
from flask_restful import Resource,reqparse,request
from datetime import datetime
from common.db_init import connect_db, close_db
from common.util import change_list_to_set_format
import psycopg2.extras
import time, re, json
parser = reqparse.RequestParser()
# parser.add_argument('key_word', type=str)
# parser.add_argument('start_date', type=datetime)
# parser.add_argument('end_date', type=datetime)
# parser.add_argument("")

parser.add_argument("token", type=str)
parser.add_argument("user_id", type=int)
parser.add_argument("house_name", type=str)
parser.add_argument("host_id", type=int)
parser.add_argument("house_id", type=int)

parser.add_argument("description", type=str)
parser.add_argument("country", type=str)
parser.add_argument("city", type=str)
parser.add_argument("suburb", type=str)
parser.add_argument("address", type=str)
parser.add_argument("type", type=str)
parser.add_argument("price", type=float)
parser.add_argument("postcode", type=int)

# lack room arrangement

parser.add_argument("room_arrangement", type=str, action='append')

parser.add_argument("common_space", type=str, action='append')
parser.add_argument("bath_number", type=int)
parser.add_argument("max_people", type=int)
parser.add_argument("amenities", type=str, action='append')

cursor, conn = connect_db()

class Item_specific_user(Resource):
    def get(self):
        args = parser.parse_args()
        if not args['user_id']:
            return {"reason": "no user id input"}, 400

        host_id = args['user_id']
        token = args['token']
        if not token:
            return {"reason": "no token"}, 400

        user_check = int(re.search(r"id(\d+)_", token).group(1))
        timepoint = float(re.sub(r'.*_', '', token))
        if time.time() - timepoint > 600:
            return {"reason" : "timeout, need login again"}
        elif host_id != user_check:
            return {"reason" : "user id in token is different from host id"}

        cursor_dict = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # cursor_dict.execute("""select * from Item where id = {}""".format(args['house_id']))
        # row = cursor_dict.fetchone()

        cursor_dict.execute("""select * from item where hoster_id = {}""".format(args['user_id']))
        rows = cursor_dict.fetchall()
        # print(rows)

        for row in rows:

            # get hoster information
            cursor.execute("""select name from user_information where id = {}""".format(row['hoster_id']))
            row['hoster_name'] = cursor.fetchone()[0]

            cursor.execute("""select position from user_photo where user_id = {}""".format(row['hoster_id']))
            temp_result = cursor.fetchone()
            if temp_result:
                row['hoster_photo'] = temp_result[0]

            cursor.execute("""select position from item_photo where item_id = {}""".format(row['id']))
            temp_result = cursor.fetchone()
            if temp_result:
                row['house_photo'] = temp_result[0]

            row['house_id'] = row.pop('id')
            row['house_name'] = row.pop('name')

            row['type'] = item_type_information.house_type_int2str(row['type'])

            for i in range(len(row['room_arrangement'])):
                for j in range(len(row['room_arrangement'][i])):
                    row['room_arrangement'][i][j] = item_type_information.bed_type_int2str(row['room_arrangement'][i][j])

            if row['common_spaces']:
                for i in range(len(row['common_spaces'])):
                    row['common_spaces'][i] = item_type_information.bed_type_int2str(row['common_spaces'][i])
            # else:
            #     del row['common_spaces']

            if row['amenities']:
                for i in range(len(row['amenities'])):
                    row['amenities'][i] = item_type_information.Amenities_int2str(row['amenities'][i])

            del row['create_date']

            row['price'] = float(row['price'])

            if row['rating_number']:
                rating_number = row['rating_number']
                row['accuracy'] /= rating_number
                row['communication'] /= rating_number
                row['cleanliness'] /= rating_number
                row['location'] /= rating_number
                row['check_in'] /= rating_number
                row['value'] /= rating_number
            del row['rating_number']

            if not row['unavailable_data']:
                del row['unavailable_data']

            row['total_rating'] = (row['accuracy'] + row['communication'] + row['cleanliness'] + \
                                   row['location'] + row['check_in'] + row['value']) / 6
        result = {}
        result['items'] = rows
        return result, 200