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

class Item(Resource):
    def post(self):
        # args = parser.parse_args()

        args = json.loads(request.data)
        if not args['house_name'] or not args['country'] or not args['city']\
            or not args['suburb'] or not args['address'] or not args['price']\
            or not args['bath_number'] or not args['max_people'] or not args['postcode']\
             or not args['room_arrangement']:
            return {"reason": "one of not null attributes is null"}, 404

        # need token information
        host_id = args['user_id']
        token = args['token']

        user_check = int(re.search(r"id(\d+)_", token).group(1))
        timepoint = float(re.sub(r'.*_', '', token))
        if time.time() - timepoint > 6000:
            return {"reason" : "timeout, need login again"}
        elif host_id != user_check:
            return {"reason" : "user id in token is different from host id"}
        # host_id = 3

        cursor.execute("""select * from item 
                         where country = '{}' 
                         and city = '{}'
                         and suburb = '{}'
                         and address = '{}'""".format(args['country'], args['city'], args['suburb'], args['address']))
        if cursor.rowcount:
            return {"reason" : "duplicate item"}, 400


        house_type_id = item_type_information.house_type_str2int(args['type'])
        if house_type_id == -1:
            return {"reason": "house_type give unreadable string"}, 400

        ## argv['room_arrangment'] = [["single", "double"], ["king"]]
        room_arrangement = []
        for i in range(len(args['room_arrangement'])):
            temp = []
            for type in args['room_arrangement'][i]:
                x = item_type_information.bed_type_str2int(type)
                if x == -1:
                    return {"reason": "room_arrangement give unreadable string"}, 400
                temp.append(x)
            # for i in range(6 - len(temp)):
            #     temp.append(0)
            room_arrangement.append(temp)

        common_space = []
        if args['common_space']:
            for i in args['common_space']:
                x = item_type_information.bed_type_str2int(i)
                if x == -1:
                    return {"reason" : "common_space give unreadable string is {}".format(args['common_space'][0])}, 400
                common_space.append(x)

        amenities = []
        for i in args['amenities']:
            x = item_type_information.Amenities_str2int(i)
            if x == -1:
                return {"reason" : "amenities give unreadable string"}, 400
            amenities.append(x)


        cursor.execute("""insert into Item(hoster_id, name, description, create_date, country, city, suburb, address,
                            post_code, type, price, accuracy, communication, cleanliness, location, check_in, value, 
                            rating_number, room_arrangement, common_spaces, bath_number, max_people, amenities)
                       values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '0', '0', '0', '0',
                       '0', '0', '0', '{}','{}', '{}', '{}', '{}') RETURNING id"""
                      .format(host_id, args['house_name'], args['description'],datetime.now(), args['country'], args['city'],
                              args['suburb'], args['address'], args['postcode'], house_type_id, args['price'],
                              change_list_to_set_format(room_arrangement), change_list_to_set_format(common_space), args['bath_number'], args['max_people'], change_list_to_set_format(amenities)))

        item_id = cursor.fetchone()[0]
        conn.commit()

        if 'photos' in args:
            for url in args['photos']:
                cursor.execute("""insert into item_photo(item_id, position) values ('{}', '{}')""".format(item_id, url))
            conn.commit()
        return {"reason" : ""}, 200


    def put(self):
        # args = parser.parse_args()
        args = json.loads(request.data)

        if not args['house_name'] or not args['country'] or not args['city']\
            or not args['suburb'] or not args['address'] or not args['price']\
            or not args['bath_number'] or not args['max_people'] or not args['postcode']\
            or not args['room_arrangement']:
            return {"reason": "one of not null attributes is null"}, 404

        if not args['house_id']:
            return {"reason" : "no house_id"}, 400

        try:
            cursor.execute("""delete from item_photo where item_id = {}""".format(args['house_id']))
        except:
            return {"reason" : "item photo error"}

        try:
            cursor.execute("""delete from Item where id = {}""".format(args['house_id']))
            conn.commit()
        except:
            return {"reason" : "house_id does not exist"}, 400




        # need token information
        host_id = args['host_id']
        token = args['token']

        user_check = int(re.search(r"id(\d+)_", token).group(1))
        timepoint = float(re.sub(r'.*_', '', token))
        if time.time() - timepoint > 6000:
            return {"reason" : "timeout, need login again"}
        elif host_id != user_check:
            return {"reason" : "user id in token is different from host id"}



        house_type_id = item_type_information.house_type_str2int(args['type'])
        if house_type_id == -1:
            return {"reason": "house_type give unreadable string"}, 400

        ## argv['room_arrangment'] = ['single,double', 'double']
        room_arrangement = []
        for i in range(len(args['room_arrangement'])):
            temp = []
            for type in args['room_arrangement'][i]:
                x = item_type_information.bed_type_str2int(type)
                if x == -1:
                    return {"reason": "room_arrangement give unreadable string"}, 400
                temp.append(x)
            room_arrangement.append(temp)

        common_space = []
        if args['common_space']:

            for i in args['common_space']:
                x = item_type_information.bed_type_str2int(i)
                if x == -1:
                    return {"reason" : "common_space give unreadable string is {}".format(args['common_space'][0])}, 400
                common_space.append(x)

        amenities = []
        for i in args['amenities']:
            x = item_type_information.Amenities_str2int(i)
            if x == -1:
                return {"reason" : "amenities give unreadable string"}, 400
            amenities.append(x)


        cursor.execute("""insert into Item(id, hoster_id, name, description, create_date, country, city, suburb, address,
                            post_code, type, price, accuracy, communication, cleanliness, location, check_in, value,
                            rating_number, room_arrangement, common_spaces, bath_number, max_people, amenities)
                       values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '0', '0', '0', '0',
                       '0', '0', '0', '{}','{}', '{}', '{}', '{}')"""
                      .format(args['house_id'], host_id, args['house_name'], args['description'],datetime.now(), args['country'], args['city'],
                              args['suburb'], args['address'], args['postcode'], house_type_id, args['price'],
                              change_list_to_set_format(room_arrangement), change_list_to_set_format(common_space), args['bath_number'], args['max_people'], change_list_to_set_format(amenities)))

        conn.commit()


        if args['photos']:
            for url in args['photos']:
                cursor.execute("""insert into item_photo(item_id, position) values ('{}', '{}')""".format(args['house_id'], url))
            conn.commit()
        return {"reason" : ""}, 200


    def get(self):
        args = parser.parse_args()
        if not args['house_id']:
            return {"reason" : "no house id input"}, 400
        cursor_dict = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor_dict.execute("""select * from Item where id = {}""".format(args['house_id']))
        row = cursor_dict.fetchone()

        # get hoster information
        cursor.execute("""select name from user_information where id = {}""".format(row['hoster_id']))
        row['hoster_name'] = cursor.fetchone()[0]

        cursor.execute("""select position from user_photo where user_id = {}""".format(row['hoster_id']))
        temp_result = cursor.fetchone()
        if temp_result:
            row['hoster_photo'] = temp_result[0]

        cursor.execute("""select position from item_photo where item_id = {}""".format(args['house_id']))
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
        return row ,200

    def delete(self):
        args = parser.parse_args()
        print(args['house_id'])
        if not args['house_id']:
            return {"reason" : "no house_id"}, 400

        try:
            cursor.execute("""delete from item_photo where item_id = {}""".format(args['house_id']))
        except:
            return {"reason" : "item photo error"}
        try:
            cursor.execute("""delete from Item where id = {}""".format(args['house_id']))
            conn.commit()
            return {"reason": ""}, 200
        except:
            return {"reason" : "house_id does not exist"}, 400

