from flask import Flask
from flask_restful import Api
from resource.user import Login,Register,Edit_profile
from resource.item import Item
from resource.message import Message
from resource.home_page_item import Home_page_item
from resource.search import Search ,Search_Post
from resource.booking import Book
from resource.trip import Trip
from resource.unavailable_date import Unavailable_date
from resource.post import Post
from resource.post_specific import Post_specific
from resource.transaction import Confirm_Host,Confirm_User
from resource.review import Review
from resource.item_specific_user import Item_specific_user
from resource.user_information import User_information
from resource.user_posts import User_posts

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

api.add_resource(Login,'/Login')
#curl "http://127.0.0.1:5000/Login" -d email="1105958064@qq.com" -d password="dalaodaiwo" -X POST

api.add_resource(Register,'/Register')
#curl "http://127.0.0.1:5000/Register" -d email="comp6715@cse.com" -d password="j123" -d name="Jayson" -d gender=M -d date_of_birth="1993-08-30" -d self_description="easy" -d photo="https://gaoxiao/photo"  -X POST

api.add_resource(Edit_profile,'/Edit-profile')
#curl "http://127.0.0.1:5000/Edit-profile" -d token=id3_1548191813 -d name="Tatumn" -d gender="M" -d phone="045777700" -d date_of_birth="1994-04-24" -d self_description="so good" -d photo="https://gaoxiao/selfies" -X PUT
#curl "http://127.0.0.1:5000/Edit-profile" -d token=id3_1548191813 -X GET

api.add_resource(Message,'/Message/<string:request>')
#curl "http://127.0.0.1:5000/Message/preview" -d token=id1_1538191813 -d user_id=1 -X GET
#curl "http://127.0.0.1:5000/Message/detail" -d token=id1_1538191813 -d user_id=1 -d receiver_id=2 -X GET
#curl "http://127.0.0.1:5000/Message/post" -d token=id1_1538191813 -d sender_id=1 -d receiver_id=2 -d message_content="I gonna have a meet with you" -d date="2018-9-30 10:23:50" -X POST

api.add_resource(Search,'/Search')
#curl "http://127.0.0.1:5000/Search" -d key_word='Sydney' -d price=100 -d price=200 -d start_date='2018-10-02' -d end_date='2018-10-04' -d type='house' -d page_number=1 -X GET
api.add_resource(Search_Post,'/SearchPost')
#curl "http://127.0.0.1:5000/SearchPost" -d key_word='Sydney' -d price=200 -d price=350 -d start_date='2018-10-20' -d end_date='2018-12-20' -d page_number=1 -X GET

api.add_resource(Book,'/Book')
#curl "http://127.0.0.1:5000/Book" -d token=id1_1548191813 -d item_id=2 -d user_id=1 -d start_date='2018-10-20' -d end_date='2018-10-23' -d date='2018-10-09' -d comment='nothing' -X POST
api.add_resource(Trip,'/Trip')
# curl "http://127.0.0.1:5000/Trip" -d token=id3_1548191813 -d user_id=3 -X GET
api.add_resource(Confirm_Host,'/Confirm/Host')
#curl "http://127.0.0.1:5000/Confirm/Host" -d token=id3_1548191813 -d host_id=3 -d transaction_id=5 -d status='accept' -X POST
api.add_resource(Confirm_User,'/Confirm/User')
#curl "http://127.0.0.1:5000/Confirm/User" -d token=id1_1548191813 -d user_id=1 -d transaction_id=2 -d status='cancel' -X POST
api.add_resource(Review,'/Review')
#curl "http://127.0.0.1:5000/Review" -d token=id1_1548191813 -d user_id=1 -d transaction_id=5 -d date='2018-10-11' -d comment='so good' -d accuracy=10 -d communication=10 -d cleanliness=10 -d location=10 -d check_in=10 -d value=10 -X POST
#curl "http://127.0.0.1:5000/Review" -d item_id=2 -X GET

api.add_resource(Item, '/Item_operation')
api.add_resource(Home_page_item, '/Home_page')
api.add_resource(Unavailable_date, '/Unavailable_date')

api.add_resource(Post, '/Posts')
api.add_resource(Post_specific,'/Post_specific')

api.add_resource(Item_specific_user, '/Item_specific_user')

api.add_resource(User_information, '/User_information')
api.add_resource(User_posts, '/User_posts')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
