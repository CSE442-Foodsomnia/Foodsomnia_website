from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
import sys
import requests
from json import dumps

from . import db
from .models import User


views = Blueprint("views", __name__)

@views.route("/")
#@login_required
def home():
    print("home!", file=sys.stdout)
    return render_template("home.html")


@views.route("/database")
def database_show():
    user_list = User.query.all()
    return render_template("database.html", user_list=user_list)


@views.route("/database-delete")
def database_delete():
    pass
