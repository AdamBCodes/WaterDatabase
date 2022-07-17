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
                #All Values that are pulled from the forms
                streetnum = request.form["streetnum"]
                street = request.form["street"]
                meterNum = request.form["meterNum"]
                meterSize = request.form["meterSize"]
                tieOne = request.form["tieOne"]
                tieTwo = request.form["tieTwo"]
                notes = request.form["notes"]

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
                    address = addresses(streetnum, street, city, meterNum, meterSize, tieOne, tieTwo, notes, image.filename)

                    #Resizes Image
                    resized = Image.open("./website/static/imgs/"+image.filename)
                    resized = resized.resize((400, 400))
                    resized.save("./website/static/imgs/"+secure_filename(image.filename))
                else:
                    #Creates Template for address to be committed
                    address = addresses(streetnum, street, city, meterNum, meterSize, tieOne, tieTwo, notes, "placeholder.png")

                #Commits to Database
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

@views.route("/make_changes/<id>", methods=["GET", "POST"])
def make_changes(id):
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        address = addresses.query.filter_by(id=id).first()
        street = streets.query.filter_by(city=address.city).all() 
        if request.method == "POST":
            #Checks if Address Exists
            NoAddressExists = addresses.query.filter_by(streetnum=request.form["streetnum"], street=request.form["street"], city=address.city).count()
            extension = os.path.splitext(address.image)[1]
            #Checks only if streetnum or streetAddress has been changed
            if(address.streetnum != request.form["streetnum"] or address.street != request.form["street"]):
                if(NoAddressExists <= 0):
                    #Changes Data
                    rename = (request.form["streetnum"] + request.form["street"]).replace(" ", "")
                    oldname = (address.streetnum + address.street).replace(" ", "")
                    address.streetnum = request.form["streetnum"]
                    address.street = request.form["street"]
                    dir = "./website/static/imgs/"

                    if((os.path.exists(dir+oldname+".png")) or (os.path.exists(dir+oldname+".jpeg")) or (os.path.exists(dir+oldname+".jpg"))):
                        os.rename("./website/static/imgs/"+address.image, "./website/static/imgs/"+rename+extension)
                    address.image = rename+extension
                else:
                    return render_template("make_changes.html", s=street, a=address, admin=user.admin, message="Address Already Exists")
            image = request.files["img"]
            #Resizes Image if it exists
            if(image.filename != ""):
                image.filename = (address.streetnum+address.street+extension).replace(" ", "")
                image.save("./website/static/imgs/"+image.filename)

                resized = Image.open("./website/static/imgs/"+image.filename)
                resized = resized.resize((400, 400))
                resized.save("./website/static/imgs/"+secure_filename(image.filename))
                address.image = (request.form["streetnum"] + request.form["street"] + extension).replace(" ", "")
                print(address.image)
            #Checks if meterNum field is empty
            if(request.form["meterNum"] != ""):
                address.meterNum = request.form["meterNum"]
            else:
                address.meterNum = None
            #Checks if meterSize field is empty
            if(request.form["meterSize"] != ""):
                address.meterSize = request.form["meterSize"]
            else:
                address.meterSize = None
            #Checks if tieOne field is empty
            if(request.form["tieOne"] != ""):
                address.tieOne = request.form["tieOne"]
            else:
                address.tieOne = None
            #Checks if tieTwo field is empty
            if(request.form["tieTwo"] != ""):
                address.tieTwo = request.form["tieTwo"]
            else:
                address.tieTwo = None
            #Checks if notes field is empty
            if(request.form["notes"] != ""):
                address.notes = request.form["notes"]
            else:
                address.notes = None
            db.session.commit()
            return render_template("make_changes.html", s=street, a=address, admin=user.admin, message="Address Successfully Modified")
        else:
            return render_template("make_changes.html", s=street, a=address, admin=user.admin)
    else:
        return redirect(url_for("auth.login"))

@views.route("/delete_address/<id>")
def delete_address(id):
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        if user.admin:
            address = addresses.query.filter_by(id=id).first()
            filename = os.path.splitext(address.image)[0]
            dir = "./website/static/imgs/"
            if(((os.path.exists(dir+filename+".png")) or (os.path.exists(dir+filename+".jpeg")) or (os.path.exists(dir+filename+".jpg"))) and address.image != "placeholder.png"):
                os.remove(dir+address.image)
            db.session.delete(address)
            db.session.commit()
            return redirect(url_for("views.addressViewer"))
        else:
            return redirect(url_for("views.home"))
    else:
         return redirect(url_for("auth.login"))

@views.route("/address/<id>")
def address(id):
    if "userid" in session:
        user = users.query.filter_by(id=session["userid"]).first()
        address = addresses.query.filter_by(id=id).first()
        return render_template("address.html", a = address, admin=user.admin)
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

#Testing########################################################################################
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