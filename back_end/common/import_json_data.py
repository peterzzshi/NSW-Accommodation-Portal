from common.db_init import connect_db, close_db
import json
import datetime
from  geopy.geocoders import Nominatim


with open('data.json', 'r') as f:
    data = json.load(f)

geolocator = Nominatim(user_agent="test")
cursor, conn = connect_db()
i = 2

for item in data:
    location = geolocator.reverse("{}, {}".format(item['latitude'], item['longitude']))
    temp_location = location.address.split(', ')
    try:
        postcode = int(temp_location[-2])
    except:
        postcode = '0'
    if postcode:
        city = temp_location[-4]
        suburbs = temp_location[-5]
        address = ",".join(temp_location[:-5])
    else:
        city = temp_location[-3]
        suburbs = temp_location[-4]
        address = ",".join(temp_location[:-4])


    a = """insert into Item(hoster_id, name, description, create_date, country, city, suburb, address, post_code, type, price,
                     accuracy, communication, cleanliness, location, check_in, value, rating_number,
                     room_arrangement, common_spaces, bath_number, max_people, amenities)
    values ('3', '{}', 'good house, do not miss', '{}', 'Australia', '{}', '{}', '{}', '{}', '1', '{}', '0', '0', '0', '0', '0', '0',
            '0', '{{{{1}}}}', '{{}}', '{}', '{}', '{{1,2,3,4,5}}')""".format(item['title'], datetime.datetime.now(), city, suburbs, address, postcode, item['price'], int(item['bathroom_num']), item['guest_num'])
    print(a)

    cursor.execute("""insert into Item(hoster_id, name, description, create_date, country, city, suburb, address, post_code, type, price,
                     accuracy, communication, cleanliness, location, check_in, value, rating_number,
                     room_arrangement, common_spaces, bath_number, max_people, amenities)
    values ('3', '{}', 'good house, do not miss', '{}', 'Australia', '{}', '{}', '{}', '{}', '1', '{}', '0', '0', '0', '0', '0', '0',
            '0', '{{{{1}}}}', '{{}}', '{}', '{}', '{{1,2,3,4,5}}')"""
                   .format(item['title'], datetime.datetime.now(), city, suburbs, address, postcode, item['price'], int(item['bathroom_num']), item['guest_num']))
    conn.commit()

    for photo in item['album']:
        cursor.execute("""insert into Item_photo(Item_id, position) values ('{}', '{}')""".format(i, photo))
    i += 1
    conn.commit()




# cursor.execute("""select * from Item(Item_id, posision) values (%s, %s)""", i, photo)
# rows = cursor.fetchall()
# print(rows)

close_db(conn)
