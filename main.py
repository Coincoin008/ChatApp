from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from markupsafe import escape
import db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["UPLOAD_FOLDER"] = "./static/download"
app.config["SECRET_KEY"] = "feiljhzhefhs;h,q"

@app.route("/")
def index():
    name = session.get("name")
    if name:
        requests = db.get_friend_request(name)
        print(requests)
        return render_template("index.html", name=name, requests=requests)
    else:
        return redirect("/login")

@app.route("/chat/<other>")
def chat(other):
    name = session.get("name")
    if name:
        return render_template("chat.html", otherOne=other)
    else:
        return redirect("/login")

@app.route("/login") # la page pour se connecter (si déjà inscrit)
def login_page(): 
    error = request.args.get("error", "")   
    return render_template("login.html", error=error)

@app.route("/login-f", methods=["POST"]) # l'url où s'executera la fonction pour se connecter
def login():
    name = request.form.get("name") # = "Nino"
    print("CCC " + name)
    password = request.form.get("password")

    users = db.get_users()   # -> [ [id, name, password], [id, name, password], ...]
    names = [user[1] for user in users]
    passwords = [user[2] for user in users]
    print(users)

    if name in names:  # s'il y a un utilisateur avec ce nom
        if passwords[names.index(name)] == password :  # si le mot de passe rentré correspond à celui du nom rentré dans la db
            session["name"] = name  # alors il se connecte
            return redirect("/") # on va à l'accueil
        else:  # si le mot de passe est incorrect
            print(f"Login: {name} s'est connecté avec un mdp incorrect")
            return redirect("/login?error=Le%20mot%20de%20passe%20est%20incorrect")
    
    else:
        print("On a essayé de se connecter avec un nom qui n'existe pas")
        return redirect("/login?error=Le%20nom%20n'existe%20pas")

@app.route("/accept_friend/<sender>")
def accept_friend_page(sender):
    name = session.get("name")
    if name:
        return render_template("confirm_friend_request.html", sender=sender)
    else:
        return redirect("/login")

@app.route("/accept_friend_/<sender>", methods=["POST"])
def accept_friend(sender):
    name = session.get("name")
    if name:
        requests = db.get_friend_request(name)
        if sender in requests:
            if request.form.get("accept") == "yes":
                db.accept_friend_request(from_=sender, to_=name)
            return redirect("/")
    else:
        return redirect("/login")

@app.route("/signup")  # la page pour créer un compte
def signup_page():
    error = request.args.get("error", "")
    return render_template("signup.html", error=error)

@app.route("/signup-f", methods=["POST"])  # l'url où s'executera la fonction pour créer un compte
def signup():
    name = request.form.get("name")  # le nom rentré dans le form
    pw1  = request.form.get("pw1") # le mot de passe
    pw2  = request.form.get("pw2") # le deuxième mot de passe ( pour vérifier

    users = db.get_users()
    names = map(lambda user: user[1], users)
    
    if name not in names:   # si le nom n'existe pas déjà
        if pw1 == pw2:   # si les deux mots de passe correspondent
            db.create_user(name, pw1)  # alors on crée l'utilisateur
            print("B")
            session["name"] = name
            return redirect("/")
        else:   # si les deux mots de passe ne correspondent pas 
            print("A")
            return redirect("/signup?error=Les%20deux%20mots%20de%20passe%20ne%20correspondent%20pas")
    else:
        return redirect("/signup?error=Ce%20nom%20est%20déjà%20utilisé")


@app.route("/users")
def users():
    users = db.get_users()
    names = map(lambda u: u[1], users)

    return "<br>".join(names)


@app.route("/friend_request", methods=["POST"])
def friend_request():
    friend_name = request.form.get("friend_name")
    current_user = db.get_user_infos(session.get("name"))
    current_name = current_user[1]
    db.add_friend_request(current_name, friend_name)

    return redirect("/")

@app.route("/logout")
def logout():
    if session.get("name"):
        session["name"] = None
        return redirect("/login")
    else:
        return redirect("/login")

if __name__ == "__main__":
    app.run(host="localhost")