from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
import psycopg2.extras
import re,time,math,datetime
import sys

parser = reqparse.RequestParser()
parser.add_argument('key_word', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('rating', type=int, action='append')
parser.add_argument('price_start', type=int)
parser.add_argument('price_end', type=int)
parser.add_argument('type', type=str)

class Search(Resource):
    def get(self):
        args = parser.parse_args()
        keywords = args['key_word']
        start = args['start_date']
        end = args['end_date']
        rating = args['rating']
        price_start = args['price_start']
        price_end = args['price_end']
        type_name = args['type']
        error = None
        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        current_time = datetime.date.today()
        cursor.execute("delete from unavailable_date where date < '{}';".format(current_time))
        conn.commit()
        
        if keywords != None:
            cursor.execute("select id,name,rating_number,price,(accuracy+communication+cleanliness+location+check_in+value)/6 as rating,type from item \
                            where UPPER(name) like upper('%{}%') or UPPER(description) like UPPER('%{}%') or UPPER(country) like UPPER('%{}%') or UPPER(city) like UPPER('%{}%') or UPPER(suburb) like UPPER('%{}%')\
                            or UPPER(address) like UPPER('%{}%');".format(keywords,keywords,keywords,keywords,keywords,keywords))
        else:
            error = 'Searching words required.'
            close_db(conn)
            return {'items': [],
                    'reason': error},400
        items = cursor.fetchall()
        items_list=[]
        
        if price_start != None and price_end != None:
            for item in items:
                if price_start <= item['price'] <= price_end:
                    items_list.append(item)
            items=items_list.copy()
            items_list.clear()

        if rating != None and len(rating)==2:
            for item in items:
                if rating[0] <= item['rating'] <= rating[1]:
                    items_list.append(item)
            items=items_list.copy()
            items_list.clear()

        if start != None and end != None:
            start = datetime.datetime.strptime(start,'%Y-%m-%d').date()
            end = datetime.datetime.strptime(end,'%Y-%m-%d').date()
            for item in items:
                cursor.execute("select date from unavailable_date where item_id = {}".format(item['id']))
                unavailable_date = cursor.fetchall()
                index=0
                for date in unavailable_date:
                    if start <= date['date'] <= end:break
                    if start <= date['date'] <= end:break
                    index += 1
                if index == len(unavailable_date): items_list.append(item)
            items=items_list.copy()
            items_list.clear()
 
        if type_name != None:    
            cursor.execute("select id from house_type where name='{}';".format(type_name))
            results = cursor.fetchall()
            if len(results) == 0:
                error = 'No such type of item.'
                close_db(conn)
                return {'items': [],
                        'reason': error},400
            else:
                itype = results[0]['id']
                for item in items:
                    if item['type'] == itype:
                        items_list.append(item)
            items = items_list.copy()
            items_list.clear()

        for item in items:
            item['price'] = float(item['price'])
            item.pop('type')
            cursor.execute("select position from item_photo where item_id = {};".format(item['id']))
            photo = cursor.fetchall()[0]['position']
            item['image'] = photo
            
        close_db(conn)
        return {'items': items,
                'reason': error},200

class Search_Post(Resource):
    def get(self):
        args = parser.parse_args()
        keywords = args['key_word']
        start = args['start_date']
        end = args['end_date']
        price_start = args['price_start']
        price_end = args['price_end']
        error = None
        cursor, conn = connect_db()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        
        if keywords != None:
            cursor.execute("select * from post \
where UPPER(country) like upper('%{}%') or UPPER(city) like UPPER('%{}%') or UPPER(suburb) like UPPER('%{}%') or UPPER(comment) like UPPER('%{}%');".format(keywords,keywords,keywords,keywords))
        else:
            error = 'Searching words required.'
            close_db(conn)
            return {'items': [],
                    'reason': error},400
        posts = cursor.fetchall()
        posts_list=[]
        
        if price_start != None and price_end:
            for post in posts:
                if price_start <= post['price_start'] <= post['price_end'] <= price_end:
                    posts_list.append(post)
            posts=posts_list.copy()
            posts_list.clear()
        if start != None and end != None:
            start = datetime.datetime.strptime(start,'%Y-%m-%d').date()
            end = datetime.datetime.strptime(end,'%Y-%m-%d').date()
            for post in posts:
                if start <= post['start_date'] <= post['end_date'] <= end:
                    posts_list.append(post)
            posts=posts_list.copy()
            posts_list.clear()

        for post in posts:
            post['end_date'] = str(post['end_date'])
            post['start_date'] = str(post['start_date'])
            post['post_date'] = str(post['post_date'])
       
        close_db(conn)
        return {'posts': posts,
                'reason': error},200
        
