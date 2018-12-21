from common.db_init import connect_db, close_db
from datetime import datetime

cursor,conn = connect_db()


# x = None
# cursor.execute("""insert into User_information(email, password, name, self_description, date_of_birth, create_date)
#                   values('{}', '{}', '{}', '{}', '{}', '{}')"""
#               .format('test_user@cse.com', 'dalaodaiwo', 'heihei', x, datetime.now(), datetime.now()))
#
# conn.commit()
# close_db(conn)
#
# cursor.execute("""select * from User_information""")
# raws = cursor.fetchall()
# for i in raws:
#     print(i)
#     if i[4]:
#         print(i[4])