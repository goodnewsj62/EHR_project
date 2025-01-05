from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.doctor.form import PatientForm, PatientRecordForm
from app.models import Image, Patient, PatientRecord
from app import db


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
    page = request.values.get("page")
    patient = Patient.query.filter_by(id=id).first()

    if not patient:
        abort(404)

    if patient.user_id != current_user.id:
        abort(403)

    records = PatientRecord.query.filter_by(patient_id=id).paginate(
        page=page, per_page=current_app.config.get("PER_PAGE", 10)
    )

    return render_template("app/patient.html", patient=patient, records=records)


@app.route("/create-patient", methods=["GET", "POST"])
@login_required
def create_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient()
        form.populate_obj(patient)
        patient.user_id = current_user.id
        db.session.add(patient)
        db.session.commit()
        flash("patient created successfully", category="success")
        return redirect(url_for("doctor.get_patient", id=patient.id))
    return render_template("app/create_patient.html", form=form, form_type="create")


@app.route("/update-patient/<id>", methods=["GET", "POST"])
@login_required
def update_patient(id):
    obj = Patient.query.filter_by(id=id).first()
    if not obj:
        abort(404)

    if obj.user_id != current_user.id:
        abort(403)

    form = PatientForm(obj=obj)
    if form.validate_on_submit():
        form.populate_obj(obj)
        db.session.commit()
        flash("patient data updated successfully", category="success")
        return redirect(url_for("doctor.get_patient", id=id))
    return render_template("app/update_patient.html", form=form, form_type="update")


@app.route("/delete-patient/<id>", methods=["POST"])
@login_required
def delete_patient(id):
    obj = Patient.query.filter_by(id=id).first()
    if not obj:
        abort(404)

    if obj.user_id != current_user.id:
        abort(403)

    db.session.delete(obj)
    db.session.commit()
    flash("patient deleted successfully", category="success")
    return redirect(url_for("doctor.dashboard"))


@app.route("/record/<id>", methods=["GET"])
@login_required
def get_record(id):
    page = request.values.get("page", 1)

    obj = Patient.query.filter_by(id=id).first()
    if not obj:
        abort(404)

    if obj.user_id != current_user.id:
        abort(403)

    records = PatientRecord.query.filter_by(patient_id=id).paginate(
        page=page, per_page=current_app.config.get("PER_PAGE", 10)
    )
    return render_template("app/records.html", records=records)


@app.route("/create-record/<id>", methods=["POST", "GET"])
@login_required
def create_patient_record(id):
    obj = Patient.query.filter_by(id=id).first()
    if not obj:
        abort(404)

    if obj.user_id != current_user.id:
        abort(403)

    form = PatientRecordForm()

    if form.validate_on_submit():
        patient = PatientRecord()
        form.populate_obj(patient)
        patient.patient_id = id
        db.session.add(patient)
        db.session.commit()
        flash("record created successfully", category="success")
        return redirect(url_for("doctor.get_patient", id=patient.id))

    return render_template("app/create_record.html", form=form)
