import psycopg2
import psycopg2.extras
from datetime import datetime

def connect_db():
    try:
        connect_str = "dbname='mini_airbnb' user='comp9900' " \
                      "host='comp9900.cowsy7ltgrbf.ap-southeast-2.rds.amazonaws.com'" \
                      "password='dalaodaiwo'"
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        # cursor.execute("""select * from User_information""")
        # rows = cursor.fetchall()
        # print(rows)
        return cursor, conn
    except:
        return None

def close_db(conn):
    conn.close()
    return




if __name__ == '__main__':
    pass
    # args = {'house_id' : 1}
    # cursor, conn = connect_db()
    # cursor.execute("""select * from unavailable_date where item_id = {}""".format(args['house_id']))
    # rows = cursor.fetchall()
    # today = datetime.now().strftime("%Y-%m-%d")
    #
    # result = {"unavailable" : []}
    # for row in rows:
    #     format_date = row[2].strftime("%Y-%m-%d")
    #     if today > format_date:
    #         print(row)
    #         try:
    #             cursor.execute("""delete from unavailable_date where id = {}""".format(row[0]))
    #             cursor.commit()
    #         except:
    #             continue
    #     else:
    #         result['unavailable'].append(format_date)
    # # if not args['start_date']:
    # #     return result
    #
    # result['unavailable'].sort()
    # start_time = args['start_date'].strftime("%Y-%m-%d")
    # if start_time > result['unavailable']:
    #     return