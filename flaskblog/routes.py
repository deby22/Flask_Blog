from flask import render_template, url_for, flash, redirect

from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


posts = [
    {
        "author": "Dawid Dęby",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2021",
    },
    {
        "author": "Dawid Dęby",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2021",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@admin.pl" and form.password.data == "admin":
            flash("You have been loged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Something goes wrong. Please check username and password", "danger")
    return render_template("login.html", title="Register", form=form)
