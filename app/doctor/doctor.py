from flask import Blueprint, abort, current_app, render_template, request
from flask_login import current_user, login_required

from app.models import Image, Patient, PatientRecord


app = Blueprint("doctor", __name__, url_prefix="/app")


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    page = request.values.get("page", 1)
    patient_query = Patient.query.filter_by(user_id=current_user.id)
    context = {}
    context["patients"] = patient_query.paginate(
        page=page, per_page=current_app.config.get("PER_PAGE", 10)
    )
    context["patient_count"] = patient_query.count()
    context["record_count"] = (
        PatientRecord.query.join(Patient, Patient.id == PatientRecord.patient_id)
        .filter(Patient.user_id == current_user.id)
        .count()
    )
    return render_template("app/dashboard.html", context=context)


@app.route("/patients/<int:id>", methods=["GET"])
@login_required
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    records = patient.records

    if not patient:
        abort(404)

    if patient.user_id != current_user.id:
        abort(403)

    return render_template("app/patient.html")


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
