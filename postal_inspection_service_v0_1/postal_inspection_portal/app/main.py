from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Investigation, Suspect, Evidence, Inspector

bp = Blueprint("main", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        investigations=Investigation.query.order_by(Investigation.opened_on.desc()).limit(8).all(),
        investigation_count=Investigation.query.count(),
        suspect_count=Suspect.query.count(),
        evidence_count=Evidence.query.count(),
        inspector_count=Inspector.query.filter_by(active=True).count(),
        current_user=current_user,
    )
