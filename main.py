import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = os.urandom(24)

MONGODB_URI = "mongodb://localhost:27017"
client = MongoClient(MONGODB_URI)
db = client["miproyecto"]
users = db["users"]
users.create_index("email", unique=True)


def hash_password(password: str) -> str:
    return str(hash(password))


def verify_password(stored_password: str, provided_password: str) -> bool:
    return str(hash(provided_password)) == stored_password


@app.route("/")
def home():
    return render_template("home.html", user=session.get("user"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm", "")

        if not name or not email or not password or not confirm_password:
            flash("Todos los campos son obligatorios.", "error")
        elif password != confirm_password:
            flash("Las contraseñas no coinciden.", "error")
        elif users.find_one({"email": email}):
            flash("Este correo electrónico ya está registrado.", "error")
        else:
            hashed_password = hash_password(password)
            users.insert_one({"name": name, "email": email, "password": hashed_password})
            session["user"] = name
            session["email"] = email
            flash("Registro exitoso. Ya estás conectado.", "success")
            return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users.find_one({"email": email})
        if user and verify_password(user["password"], password):
            session["user"] = user["name"]
            session["email"] = user["email"]
            flash(f"Bienvenido de nuevo, {user['name']}!", "success")
            return redirect(url_for("profile"))

        flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/profile")
def profile():
    if not session.get("user"):
        flash("Debes iniciar sesión para ver tu perfil.", "error")
        return redirect(url_for("login"))

    return render_template("profile.html", user=session["user"], email=session.get("email"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
