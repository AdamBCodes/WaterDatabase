from flask import Blueprint, render_template, url_for, redirect

public = Blueprint("public", __name__, static_folder="static", template_folder="templates/public")

@public.route("/")
def index():
    return render_template("index.html")