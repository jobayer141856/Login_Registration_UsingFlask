from flask import Flask, request, redirect, render_template, session
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

users_table = mydb["users"]
 
app = Flask(__name__)

@app.route('/register', methods=['GET', "POST"])
def register():
    is_post = False
    p = False
    u = False
    pl = False
    r = False
    username = None
    password1 = None
    pass_length= None
    if request.method == "POST":
        is_post = True
        form_data = dict(request.form)
        form_username = form_data["username"]
        form_name = form_data["name"]
        nameOfU = str(form_name)
        print(nameOfU)
        form_password = form_data["password"]
        form_Conf_password = form_data["conf_password"]
        form_gmail = form_data["email"]

        print(form_data)

        db_user = users_table.find_one({"username": form_username})

        print(db_user)

        if db_user is not None:
            username = 'User already exist'
            u = True
        if db_user is None:
            if form_password != form_Conf_password:
                p = True
                password1 = 'Password does not match. Please enter correct password'

        if password1 is None:
            if len(form_password)<6:
                pass_length = 'Password length must be 6 or greater than 6'
                pl = True

        if(pass_length is None ) and (username is None ) and (password1 is None):
            users_table.insert_one({"name": form_name, "username": form_username,  "gmail": form_gmail , "password": form_password})
            r = True

    return render_template("registration.html", **locals())

    

@app.route('/', methods=['GET', "POST"])
def index():
    is_post = False
    username = False
    password = False
    p = 'exist'
    u = 'exist'
    if request.method == "POST":
        is_post = True
        form_data = dict(request.form)
        form_username = form_data["username"]
        form_password = form_data["password"]
        print(form_data)
        db_user = users_table.find_one({"username": form_username})
        if db_user is None:
            username = True
            u = None
        if db_user is not None:
            if form_password != db_user["password"]:
                password = True
                p = None

        if (p is not None) and (u is not None):
            name = db_user["name"]
            return render_template("home.html" , **locals())

    return render_template("login.html", **locals())



if __name__ == '__main__':
    app.run(debug=True)
