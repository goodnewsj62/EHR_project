from typing import List
from functools import partial
import datetime
import enum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str]
    email_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    date_created: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc)
    )
    patients: Mapped[List["Patient"]] = relationship(back_populates="creator")


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    BISEXUAL = "bi-sexual"
    OTHERS = "others"


class Patient(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    address: Mapped[str]
    age: Mapped[int]
    gender: Mapped[Gender]
    ethnicity: Mapped[str] = mapped_column(String(40), nullable=False)
    date_created: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc)
    )
    records: Mapped[List["PatientRecord"]] = relationship(back_populates="patient")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="patients")


class PatientRecord(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    is_immunized: Mapped[bool] = mapped_column(default=False)
    appointment: Mapped[datetime.datetime]
    date_created: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc)
    )
    patient_id: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    images: Mapped[List["Image"]] = relationship(back_populates="record")
    patient: Mapped["Patient"] = relationship(back_populates="records")


class Image(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    blob: Mapped[str]
    date_created: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc)
    )
    record_id: Mapped[int] = mapped_column(ForeignKey("patient_record.id"))
    record: Mapped["PatientRecord"] = relationship(back_populates="images")
