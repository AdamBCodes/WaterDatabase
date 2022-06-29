############################
#        Views Page        #
# Author: Adam Barnard     #
# Date:   5/27/22          #
############################


from flask import Blueprint, render_template, url_for, redirect, request, session
from werkzeug.utils import secure_filename
import os
from PIL import Image
from uuid import uuid4
from hashlib import md5
from .models import users, cities, streets, addresses
from . import db
import time

views = Blueprint("views", __name__, static_folder="static", template_folder="templates/dashboard")


#Home Page
@views.route("/")
def home():
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        return render_template("home.html", username=user.username, admin=user.admin)
    return redirect(url_for("auth.login"))

#Page to Add Cities to database
@views.route("/add_city", methods=["POST"])
def add_city():
    if "userid" in session:
        try:
            cityName = request.form["cityName"]
            cityExists = cities.query.filter_by(name=cityName).first()
            if cityExists:
                return redirect(url_for("views.admin_page"))
            else:
                city = cities(cityName)
                db.session.add(city)
                db.session.commit()
                return redirect(url_for("views.admin_page"))
        except:
            return redirect(url_for("views.error"))
    else:
        return redirect(url_for("auth.login"))


#Page to Add Streets to database
@views.route("/add_street", methods=["POST"])
def add_street():
    if "userid" in session:
        try:
            #Gets all cities from the database
            allCities = cities.query.all()

            cityName = request.form["cName"]
            revisedName = request.form["streetName"]+" "+request.form["streetType"]
            streetExists = streets.query.filter_by(city=cityName, name=revisedName).first()
            #Check if street already exists
            if streetExists:
                message = "Street Already Exists"
                return redirect(url_for("views.admin_page"))
            else:
                street = streets(revisedName, cityName)
                db.session.add(street)
                db.session.commit()
                message="street was created"
                return redirect(url_for("views.admin_page"))
        except:
            return redirect(url_for("views.error"))
    else:
        return redirect(url_for("auth.login"))


#Page to Add Addresses to database
@views.route("/add_address/<city>", methods=["GET", "POST"])
def add_address(city):
    if "userid" in session:
        try:
            allStreets = streets.query.filter_by(city=city).all()
            #On POST
            if request.method == "POST":
                streetnum = request.form["streetnum"]
                street = request.form["street"]
                image = request.files["img"]
                addressExists = addresses.query.filter_by(city=city, street=street,streetnum=streetnum).first()
                #Checks if Address already exists
                if addressExists:
                    message="Address Already Exists"
                    return render_template("add_address.html", allStreets=allStreets, message=message)
                #Gets File Extension for image
                if(image.filename != ""):
                    extension = os.path.splitext(image.filename)[1]
                    image.filename = (streetnum+street+extension).replace(" ", "")
                    image.save("./website/static/imgs/"+secure_filename(image.filename))
                    address = addresses(streetnum, street, city, image.filename)

                    #Resizes Image
                    resized = Image.open("./website/static/imgs/"+image.filename)
                    resized = resized.resize((400, 400))
                    resized.save("./website/static/imgs/"+secure_filename(image.filename))
                else:
                    address = addresses(streetnum, street, city, "placeholder.png")
                print(address.image)
                db.session.add(address)
                db.session.commit()
                message="Successfully Created Address"
                return render_template("add_address.html", allStreets=allStreets, message=message)
            #On GET
            else:
                if len(allStreets) > 0:
                    return render_template("add_address.html", allStreets=allStreets)
                else:
                    return redirect(url_for("views.add_street"))
        except:
            return redirect(url_for("views.error"))
    else:
        return redirect(url_for("auth.login"))


@views.route("/addresses")
def addressViewer():
    if "userid" in session:
        try:
            user = users.query.filter_by(id=session["userid"]).first()
            address = addresses.query.all()
            return render_template("addresses.html", admin=user.admin, allAddresses=address)
        except:
            return redirect(url_for("views.error"))
    else:
        return redirect(url_for("auth.login"))

@views.route("/make_changes")
def make_changes():
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        return render_template("make_changes.html", admin=user.admin)
    else:
        return redirect(url_for("auth.login"))

@views.route("/admin")
def admin_page():
    if 'userid' in session:
        try:
            user = users.query.filter_by(id=session["userid"]).first()
            allCities = cities.query.all()
            allStreets = streets.query.all()
            if(user.admin):
                return render_template("admin_page.html", admin=user.admin, allCities=allCities, allStreets=allStreets)
            else:
                return redirect(url_for("views.home"))
        except:
            return redirect(url_for("views.error"))
    else:
        return redirect(url_for("auth.login"))


#Creates Users(Reworked?)
@views.route("/create_user", methods=["POST"])
def create_user():
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        isAdmin = user.admin
        if isAdmin:
            id = str(uuid4())
            username = request.form["username"]
            password = request.form["password"]
            #Encrypts password with md5 hash
            password = md5(password.encode("utf-8")).hexdigest()
            usr = users(id, username, password, False)
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for("views.admin_page"))
        else:
            return redirect(url_for("auth.login"))
    else:
        return redirect(url_for("auth.login"))



#FOR ERRORS
@views.route("/error")
def error():
    return render_template("error.html")

#Tests########################################################################
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
        print(user.id)
        print(user.username)
        print(user.password)
    return "Check Logs"

#Shows Cities(Test)
@views.route("/show_cities")
def show_cities():
    for city in cities.query.all():
        print(city.name)
    return "Check Logs"
################################################################################################