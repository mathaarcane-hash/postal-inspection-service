from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import Inspector

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        inspector = Inspector.query.filter_by(username=username, active=True).first()
        if inspector and inspector.check_password(password):
            login_user(inspector)
            return redirect(url_for("main.dashboard"))
        flash("Identifiants invalides ou compte désactivé.", "error")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
