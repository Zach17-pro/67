from flask import Blueprint, render_template, redirect, url_for, session, flash

role_page_api = Blueprint("role_page", __name__)

def _require_role(expected: str):
    user = session.get("user")
    if not user or user.get("role") != expected:
        flash("Access denied!")
        return redirect(url_for("auth.home"))
    return None

@role_page_api.get("/Admin")
def Admin():
    guard = _require_role("Admin")
    if guard: return guard
    return render_template("Admin.html", user=session["user"])

@role_page_api.get("/Platform_Manager")
def Platform_Manager():
    guard = _require_role("Platform_Manager")
    if guard: return guard
    return render_template("platformManager.html", user=session["user"])

@role_page_api.get("/Csr_Rep")
def Csr_Rep():
    guard = _require_role("Csr_Rep")
    if guard: return guard
    return render_template("csrRep.html", user=session["user"])

@role_page_api.get("/PIN_Support")
def PIN_Support():
    guard = _require_role("PIN_Support")
    if guard: return guard
    return render_template("PIN_Support.html", user=session["user"])
