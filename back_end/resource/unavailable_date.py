from flask_restful import Resource,reqparse
from common.db_init import connect_db, close_db
from datetime import datetime, timedelta

parser = reqparse.RequestParser()

parser.add_argument("house_id", type=int)
parser.add_argument("start_date", type=str)


class Unavailable_date(Resource):
    def get(self):
        args = parser.parse_args()
        if not args['house_id']:
            return {"reason" : "no house id"}, 400

        cursor, conn = connect_db()
        cursor.execute("""select * from unavailable_date where item_id = {}""".format(args['house_id']))
        rows = cursor.fetchall()
        today = datetime.now().strftime("%Y-%m-%d")

        result = {"unavailable": []}
        for row in rows:
            format_date = row[2].strftime("%Y-%m-%d")
            if today > format_date:
                print(row)
                try:
                    cursor.execute("""delete from unavailable_date where id = {}""".format(row[0]))
                    cursor.commit()
                except:
                    continue
            else:
                result['unavailable'].append(format_date)
        if not args['start_date']:
            return result

        result['unavailable'].sort()
        start_time = args['start_date']
        if start_time > result['unavailable'][-1]:
            return {"unavailable" : []}, 200
        else:
            for end_d in result["unavailable"]:
                if end_d > start_time:
                    end_date = end_d
                    break
            return {"unavailable" : [(datetime.strptime(end_date, "%Y-%m-%d") + timedelta(n)).strftime("%Y-%m-%d") for n in range(60)]}