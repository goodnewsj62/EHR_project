from datetime import datetime, timezone
import os
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
from werkzeug.utils import secure_filename

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

    record = PatientRecord.query.filter_by(id=id).first()
    if not record:
        abort(404)

    if record.patient.user_id != current_user.id:
        abort(403)

    return render_template("app/record.html", record=record)


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

        record = PatientRecord()
        form.populate_obj(record)
        naive_datetime = datetime.combine(
            form.appointment_date.data, form.appointment_time.data
        )
        utc_datetime = naive_datetime.replace(tzinfo=timezone.utc)
        record.appointment = utc_datetime
        record.patient_id = id
        db.session.add(record)

        paths = []
        try:
            for (
                f
            ) in (
                form.photos.data
            ):  # form.photo.data return a list of FileStorage object
                if f.filename:
                    filename = (
                        f"{datetime.now().isoformat(timespec='seconds')}-"
                        + secure_filename(f.filename)
                    )
                    upload_folder = os.path.join(
                        os.path.dirname(current_app.root_path), "assets", "images"
                    )
                    path = os.path.join(upload_folder, filename)
                    paths.append(path)
                    try:
                        os.makedirs(
                            upload_folder, exist_ok=True
                        )  # Handle existing directory gracefully
                    except OSError as e:
                        print(f"Error creating upload directory: {e}")
                        return None
                    f.save(path)
                    db.session.add(Image(path=path, filename=filename, record=record))

            db.session.commit()
            flash("record created successfully", category="success")
            return redirect(url_for("doctor.get_patient", id=id))

        except Exception as e:
            for path in paths:
                os.remove(path)

            print(e)
            flash("error creating record", category="error")

    return render_template("app/create_record.html", form=form)


@app.route("/update-record/<id>", methods=["POST", "GET"])
@login_required
def update_patient_record(id):
    obj = PatientRecord.query.filter_by(id=id).first()
    if not obj:
        abort(404)

    if obj.patient.user_id != current_user.id:
        abort(403)

    form = PatientRecordForm(obj=obj)

    if form.validate_on_submit():

        record = PatientRecord()
        form.populate_obj(record)
        naive_datetime = datetime.combine(
            form.appointment_date.data, form.appointment_time.data
        )
        utc_datetime = naive_datetime.replace(tzinfo=timezone.utc)
        record.appointment = utc_datetime
        db.session.add(record)

        paths = []
        try:
            for (
                f
            ) in (
                form.photos.data
            ):  # form.photo.data return a list of FileStorage object
                if f.filename:
                    filename = (
                        f"{datetime.now().isoformat(timespec='seconds')}-"
                        + secure_filename(f.filename)
                    )
                    upload_folder = os.path.join(
                        os.path.dirname(current_app.root_path), "assets", "images"
                    )
                    path = os.path.join(upload_folder, filename)
                    paths.append(path)
                    try:
                        os.makedirs(
                            upload_folder, exist_ok=True
                        )  # Handle existing directory gracefully
                    except OSError as e:
                        print(f"Error creating upload directory: {e}")
                        return None
                    f.save(path)
                    db.session.add(Image(path=path, filename=filename, record=record))

            db.session.commit()
            flash("record created successfully", category="success")
            return redirect(url_for("doctor.get_record", id=id))

        except Exception as e:
            for path in paths:
                os.remove(path)

            print(e)
            flash("error creating record", category="error")

    return render_template("app/update_record.html", form=form)


@app.route("/record/<id>", methods=["POST"])
@login_required
def delete_record(id):

    record = PatientRecord.query.filter_by(id=id).first()
    patient_id = record.patient_id
    if not record:
        abort(404)

    if record.patient.user_id != current_user.id:
        abort(403)

    try:
        for image in record.images:
            os.remove(image.path)
        db.session.delete(image)
        db.session.commit()
    except:
        flash("error deleting record", category="error")

    db.session.delete(record)
    db.session.commit()

    return redirect(url_for("doctor.get_patient", id=patient_id))


@app.route("/image/<id>", methods=["POST"])
@login_required
def delete_image(id):

    image = Image.query.filter_by(id=id).first()
    record_id = image.record_id

    if not image:
        abort(404)

    if image.record.patient.user_id != current_user.id:
        abort(403)

    try:
        os.remove(image.path)
        db.session.delete(image)
        db.session.commit()
    except:
        flash("error deleting image", category="error")

    return redirect(url_for("doctor.get_record", id=record_id))
