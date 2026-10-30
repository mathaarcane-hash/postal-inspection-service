import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
    database_url = os.environ.get("DATABASE_URL", "sqlite:///postal_inspection.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("COOKIE_SECURE", "false").lower() == "true"

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour consulter les archives."

    from app import models
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.route("/")
    def index():
        endpoint = "main.dashboard" if login_manager._login_disabled is False else "auth.login"
        return redirect(url_for("auth.login"))

    @app.cli.command("init-db")
    def init_db_command():
        """Create database tables for the initial development deployment."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command("create-admin")
    def create_admin_command():
        """Create the first administrator interactively."""
        import getpass
        from app.models import Inspector
        if Inspector.query.filter_by(role="admin").first():
            print("An administrator already exists.")
            return
        username = input("Admin username: ").strip()
        full_name = input("Full name: ").strip()
        password = getpass.getpass("Password (12+ characters): ")
        if not username or not full_name or len(password) < 12:
            print("Username and name are required; password must be at least 12 characters.")
            return
        user = Inspector(username=username, full_name=full_name, rank="Administrateur", role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("Administrator account created.")

    return app
