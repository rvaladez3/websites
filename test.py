from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = "natural disasters"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db.init_app(app)

#create db model
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name =db.Column("name", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), nullable = False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
#create funciton to return a string when we add 
    def __repr__(self):
        return '<Name %r>' % self.id # %r is prints out the integer


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user  # this is used to stores data as a dictionary
        return redirect(url_for("user"))
    else:
        return render_template("login.html")
# @app.route("/earthquake", methods=["POST", "GET"])

# def earthquake():
#     if request.method == "POST":
#         user = request.form["nm"]
#         if user == "earthquake":
#             return redirect(url_for("user", usr = user))
#     else:
#         return render_template("login.html")


#below is for users

@app.route("/Dnearby", methods=["GET"])
def Dnearby():
  # this is used to stores data as a dictionary
        return render_template("Dnearby.html")

@app.route("/disasters", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved for future notifications!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email = email)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("you have been logged out!", "info")
    return redirect(url_for("login"))
if __name__ == "__main__":
    # db.creat_all()
    app.run(debug = True)