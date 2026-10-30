from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Inspector(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(140), nullable=False)
    rank = db.Column(db.String(80), nullable=False, default="Inspecteur")
    role = db.Column(db.String(30), nullable=False, default="inspector")
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Inspector, int(user_id))


class Investigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(40), unique=True, nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(100), nullable=False, default="Autre")
    status = db.Column(db.String(40), nullable=False, default="Ouverte")
    priority = db.Column(db.String(30), nullable=False, default="Normale")
    location = db.Column(db.String(180))
    summary = db.Column(db.Text)
    opened_on = db.Column(db.Date, nullable=False, default=date.today)
    lead_inspector_id = db.Column(db.Integer, db.ForeignKey("inspector.id"))
    lead_inspector = db.relationship("Inspector", backref="led_investigations")


class Suspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(160), nullable=False)
    aliases = db.Column(db.String(240))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False, default="À identifier")
    notes = db.Column(db.Text)
    investigation_id = db.Column(db.Integer, db.ForeignKey("investigation.id"))
    investigation = db.relationship("Investigation", backref="suspects")


class Evidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    collected_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    collected_by_id = db.Column(db.Integer, db.ForeignKey("inspector.id"))
    investigation_id = db.Column(db.Integer, db.ForeignKey("investigation.id"))
    investigation = db.relationship("Investigation", backref="evidence")


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    report_type = db.Column(db.String(80), nullable=False, default="Rapport d'enquête")
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("inspector.id"))
    investigation_id = db.Column(db.Integer, db.ForeignKey("investigation.id"))
    investigation = db.relationship("Investigation", backref="reports")


class Warrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    subject_name = db.Column(db.String(160), nullable=False)
    warrant_type = db.Column(db.String(80), nullable=False, default="Mandat d'arrêt")
    status = db.Column(db.String(50), nullable=False, default="En attente")
    issued_on = db.Column(db.Date)
    expires_on = db.Column(db.Date)
    details = db.Column(db.Text)
    investigation_id = db.Column(db.Integer, db.ForeignKey("investigation.id"))
    investigation = db.relationship("Investigation", backref="warrants")
