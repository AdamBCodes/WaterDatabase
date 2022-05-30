from flask import Blueprint, render_template, session, url_for, redirect, request, session
from uuid import uuid4
from hashlib import md5
from .models import users
from . import db

views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


#Home Page
@views.route("/")
def home():
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        return render_template("home.html", username=user.username, admin=user.admin)
    return redirect(url_for("auth.login"))

#Page to Add Cities to database
@views.route("/add_city", methods=["GET", "POST"])
def add_city():
    return render_template("add_city")

#Page to Add Streets to database
@views.route("/add_street", methods=["GET", "POST"])
def add_street():
    return render_template("add_street")

#Page to Add Addresses to database
@views.route("/add_address", methods=["GET", "POST"])
def add_address():
    return render_template("add_address")



#Tests
#Creates Users(Rework Later)
@views.route("/create_user/<username>/<password>")
def create_user(username, password):
    id = str(uuid4())
    password = md5(password.encode("utf-8")).hexdigest()
    usr = users(id, username, password, False)
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for("auth.login"))

#Creates Admin
@views.route("/create_admin")
def create_admin():
    id = str(uuid4())
    username = "admin"
    password = md5("1234".encode("utf-8")).hexdigest()
    admin = True
    usr = users(id, username, password, admin)
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for("auth.login"))
    
#Shows Users(Test)
@views.route("/show_users")
def show_users():
    for user in users.query.all():
        print(user.username)
        print(user.password)
        print(user.id)
    return "Check Logs"