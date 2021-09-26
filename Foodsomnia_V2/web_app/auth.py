from flask import Blueprint, flash, render_template, redirect, url_for
from . import db
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sys
#

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    print("login!", file=sys.stdout)

    form = LoginForm()

    if form.validate_on_submit():
        print("form validated!", file=sys.stdout)

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                db.session.add(user)
                db.session.commit()
                flash("Log in successfully")
                return redirect(url_for("views.home"))

        else:
            flash("Invalid username or password")


    return render_template("login.html", form=form)



@auth.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        print("register form validated!", file=sys.stdout)

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        milk_allerg=form.milk_allerg.data,
                        peanut_allerg=form.peanut_allerg.data,
                        soybeans_allerg=form.soybeans_allerg.data,
                        wheat_allerg=form.wheat_allerg.data,
                        egg_allerg=form.egg_allerg.data,
                        fish_allerg=form.fish_allerg.data,
                        shellfish_alleg=form.shellfish_alleg.data)

        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully!")
        print("User created successfully!", file=sys.stderr)
        return redirect(url_for('auth.login'))

    return render_template("register.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))
