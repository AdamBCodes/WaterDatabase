#File to seperate Authentication from main pages
from flask import Blueprint, render_template, url_for, redirect, request, session
from hashlib import md5
from .models import users

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates/auth")

#Login Page
@auth.route("/login", methods=["GET", "POST"])
def login():
    #Checks if already logged in
    if "user" in session:
        return redirect(url_for("home"))
    else:
        #On POST
        if request.method == "POST":
            #Sets the session cookie and then redirects to home page
            username = request.form["un"]
            password = request.form["pass"]
            found_user = users.query.filter_by(username=username).first()
            encryptedPass = md5(password.encode("utf-8")).hexdigest()
            if found_user and found_user.password == encryptedPass:
                    session["userid"] = found_user.id
            else:
                error = "Invalid Username or Password"
                return render_template("login.html", error=error)
            return redirect(url_for("views.home"))
        #On GET
        else:
            #Returns the login template if not submitted
            return render_template("login.html")

#Logout Page
@auth.route("/logout")
def logout():
    session.pop("userid", None)
    return redirect(url_for("auth.login"))