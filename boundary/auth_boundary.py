from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from entity.user_repository import UserRepository
from control.auth_controller import AuthController

auth_api = Blueprint("auth", __name__)

def controller() -> AuthController:
    return AuthController(UserRepository(current_app.config["DB"]))

@auth_api.get("/")
def home():
    if "user" in session:
        role = session["user"]["role"]
        endpoint = controller().role_endpoint_for(role)
        if endpoint:
            return redirect(url_for(endpoint))
        return redirect(url_for("auth.home"))
    return render_template("login.html")

@auth_api.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    profile = request.form["profiles"]

    user = controller().authenticate(username=username, password=password, role=profile)
    if user:
        session["user"] = user
        flash(f"Welcome, {user['full_name']} ({user['role']})!")
        endpoint = controller().role_endpoint_for(user["role"])
        return redirect(url_for(endpoint)) if endpoint else redirect(url_for("auth.home"))
    flash("Invalid credentials!")
    return redirect(url_for("auth.home"))

@auth_api.get("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!")
    return redirect(url_for("auth.home"))
