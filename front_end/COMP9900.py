from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import json
import datetime

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def home_page():
    if not session.get('token'):
        flash("You are not logged in yet, log in for more features.")
    return render_template("index.jinja2")


@app.route('/host')
def host():
    url = "http://13.210.33.67:5000/Posts"
    posts = requests.get(url).json()["posts"]

    return render_template("host.jinja2", posts=posts)


@app.route('/traveller')
def traveller():
    url = "http://13.210.33.67:5000/Home_page?page_number=1"
    items = requests.get(url).json()["items"]

    return render_template("traveller.jinja2", items=items)


@app.route('/login', methods=["GET", "POST"])
def login():
    url = "http://13.210.33.67:5000/Login"

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        data = {
            "email": email,
            "password": password
        }

        response = requests.post(url, data)
        session['token'] = response.json()["token"]

        print(response.json())
        if session.get('token'):
            session['user_id'] = response.json()["user_id"]
            session['photo'] = response.json()["photo"]
            session['name'] = response.json()["name"]
            flash("Login successful, welcome!")

            return redirect(url_for("home_page"))
        else:
            flash("Wrong email or password!")

    return render_template("login.jinja2")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home_page"))



@app.route('/signup', methods=["GET", "POST"])
def signup():
    url = "http://13.210.33.67:5000/Register"

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        gender = request.form["gender"]
        description = request.form["description"]
        dob = request.form["dob"]
        phone = request.form["phone"]
        photo = request.form["photo"]

        data = {
            "email": email,
            "password": password,
            "name": name,
            "gender": gender,
            "date_of_birth": dob,
            "self_description": description,
            "phone": phone,
            "photo": photo
        }
        print(data)

        response = requests.post(url, data).json()

        if response["reason"]:
            flash(response["reason"])
        else:
            flash("Sign up successful!")
            return redirect(url_for("login"))

    return render_template("signup.jinja2")


@app.route('/profiles/<id>')
def profile(id):
    # title: name's profile
    title = "user" + id
    url = "http://13.210.33.67:5000/Edit-profile?token=" + session["token"]
    content = requests.get(url).json()

    return render_template("profile.jinja2", title=title, id=id, content=content)


@app.route('/profiles/<id>/edit', methods=["GET", "POST"])
def edit_profile(id):
    title = "Edit profile"

    url = "http://13.210.33.67:5000/Edit-profile?token=" + session["token"]
    content = requests.get(url).json()

    name = content["name"]
    gender = content["gender"]
    phone = content["phone"]
    dob = content["date_of_birth"]
    description = content["self_description"]
    photo = content["photo"]

    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        dob = request.form["dob"]
        description = request.form["description"]
        photo = request.form["photo"]

        data = {
            "token": session["token"],
            "name": name,
            "gender": gender,
            "phone": phone,
            "date_of_birth": dob,
            "self_description": description,
            "photo": photo
        }
        print(data)
        url = "http://13.210.33.67:5000/Edit-profile"
        response = requests.put(url, data)
        print(response.json())

        session['photo'] = photo
        session['name'] = name

        return redirect(url_for("profile", id=session["user_id"]))

    return render_template("edit_profile.jinja2", content=content, title=title, id=id, name=name, gender=gender, phone=phone, dob=dob, description=description, photo=photo)


@app.route('/rooms')
def rooms():

    url = 'http://13.210.33.67:5000/Item_specific_user?token=' + session["token"] + "&user_id=" + str(session["user_id"])
    response = requests.get(url)
    print(response.status_code)
    items = requests.get(url).json().get("items")
    return render_template("rooms.jinja2", items=items)


@app.route('/rooms/<id>')
def room(id):
    # each room
    url = "http://13.210.33.67:5000/Item_operation?house_id=" + id

    content = requests.get(url).json()

    print(content)

    title = content["house_name"]
    type = content["type"]
    price = content["price"]
    description = content["description"]
    photo = content['house_photo']

    city = content["city"]
    suburb = content["suburb"]
    address = content["address"]

    # host_name = content["hoster_name"]
    hoster_id = content["hoster_id"]

    return render_template("room.jinja2", content=content, home_id=id, hoster_id=hoster_id, title=title, type=type, price=price, description=description, photo=photo, city=city, suburb=suburb, address=address)


@app.route('/add_room/', methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        house_name = request.form["house_name"]
        description = request.form["description"]
        address = request.form["address"]

        photos = request.form["photos"]

        suburb = request.form["suburb"]
        city = request.form["city"]
        postcode = request.form["postcode"]
        type = request.form.get("type")
        price = request.form["price"]
        room_arrangement = request.form.getlist("room_arrangement")
        common_space = request.form.getlist("common_space")
        bath_number = request.form["bath_number"]
        max_people = request.form["max_people"]
        amenities = request.form.getlist("amenities")

        if not common_space:
            common_space = ""

        data = {
            "token": session["token"],
            "user_id": session["user_id"],
            "house_name": house_name,
            "description": description,
            "photos": photos.strip().split("\r\n"),
            "country": "Australia",
            "city": city,
            "suburb": suburb,
            "address": address,
            "type": type,
            "price": price,
            "postcode": int(postcode),

            "room_arrangement": [room_arrangement],
            "common_space": common_space,
            "bath_number": int(bath_number),
            "max_people": int(max_people),
            "amenities": amenities
        }

        url = "http://13.210.33.67:5000/Item_operation"

        response = requests.post(url, json.dumps(data))

        if response.status_code == 200:
            return redirect(url_for("rooms"))
        else:
            flash(response.json()["reason"].capitalize())

        print(response.json())
        print(response.status_code)

    return render_template("add_room.jinja2")


@app.route('/rooms/<id>/edit', methods=["GET", "POST"])
def edit_room(id):

    url = "http://13.210.33.67:5000/Item_operation?house_id=" + id
    content = requests.get(url).json()
    print(content)

    if request.method == "POST":

        house_name = request.form["house_name"]
        description = request.form["description"]
        photos = request.form["photos"]

        type = request.form.get("type")
        price = request.form["price"]
        room_arrangement = request.form.getlist("room_arrangement")
        common_space = request.form.getlist("common_space")
        bath_number = request.form["bath_number"]
        max_people = request.form["max_people"]
        amenities = request.form.getlist("amenities")

        data = {
            "token": session["token"],
            "house_id": id,
            "host_id": content["hoster_id"],
            "house_name": house_name,
            "description": description,
            "photos": photos.strip().split("\r\n"),
            "country": "Australia",
            "city": content["city"],
            "suburb": content["suburb"],
            "address": content["address"],
            "postcode": content["post_code"],
            "type": type,
            "price": price,

            "room_arrangement": [room_arrangement],
            "common_space": common_space,
            "bath_number": bath_number,
            "max_people": max_people,
            "amenities": amenities,
        }

        print(data)

        response = requests.put(url, json.dumps(data))

        print(response.json())
        print(response.status_code)

        if response.status_code == 200:
            return redirect(url_for("rooms"))
        else:
            flash(response.json()["reason"].capitalize())

    return render_template("edit_room.jinja2", id=id, content=content)


@app.route('/search_results/<keyword>', methods=["GET"])
def search_results(keyword):
    url = "http://13.210.33.67:5000/Search?key_word=" + keyword
    content = requests.get(url).json()

    items = content.get("items")
    print(items)

    return render_template("search_results.jinja2", keyword=keyword, items=items)


@app.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        print(keyword)
        return redirect(url_for("search_results", keyword=keyword))




@app.route('/posts')
def posts():

    url = "http://13.210.33.67:5000/Post_specific?token=" + session["token"] + "&user_id=" + str(session["user_id"])

    posts = requests.get(url).json()["Post"]

    return render_template("posts.jinja2", posts=posts)


@app.route('/add_post', methods=["GET", "POST"])
def add_post():

    if request.method == "POST":
        city = request.form["city"]
        suburb = request.form["suburb"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        price_start = request.form["price_start"]
        price_end = request.form["price_end"]
        people_number = request.form["people_number"]
        comment = request.form["comment"]

        data = {
            "token": session["token"],
            "user_id": session["user_id"],
            "country": "Australia",
            "city": city,
            "suburb": suburb,
            "post_date": datetime.datetime.now().strftime("%m-%d-%Y"),
            "start_date": start_date,
            "end_date": end_date,
            "price_start": price_start,
            "price_end": price_end,
            "people_number": people_number,
            "comment": comment
        }

        url = "http://13.210.33.67:5000/Posts"
        response = requests.post(url, data)

        if response.status_code == 200:
            return redirect("posts")

    return render_template("add_post.jinja2")


@app.route('/reservations/')
def reservations():
    url = "http://13.210.33.67:5000/Trip?token=" + session["token"] + "&user_id=" + str(session["user_id"])
    reservations = requests.get(url).json()["transaction"]
    print(reservations)

    return render_template("reservations.jinja2", reservations=reservations)



@app.route('/inbox/')
def messages():
    title = "all the messages here"
    return render_template("messages.jinja2", title=title)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
