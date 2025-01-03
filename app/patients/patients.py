from flask import Blueprint, abort, current_app, render_template, request
from flask_login import current_user, login_required

from app.models import Patient


app = Blueprint("ehr", __name__)


@app.route("/patients", methods=["GET"])
@login_required
def list_patient():
    page = request.values.get("page", 1)
    patients = Patient.query.filter_by(user_id=current_user.id).paginate(
        page, current_app.config.get("PER_PAGE", 10)
    )
    return render_template()


@app.route("/patients/<int:id>", methods=["GET"])
@login_required
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()

    if not patient:
        abort(404)

    if patient.user_id != current_user.id:
        abort(403)

    return render_template()


def create_patient():
    pass


def update_patent():
    pass


def delete_patient():
    pass


def list_patient_record():
    page = request.values.get("page", 1)
    patients = Patient.query.filter_by(user_id=current_user.id).paginate(
        page, current_app.config.get("PER_PAGE", 10)
    )
    return render_template()


def create_patient_record():
    pass
