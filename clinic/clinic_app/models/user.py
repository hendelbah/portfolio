"""
This module contains User model class, that also is a class for authorization in web app
"""
from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin
from werkzeug.security import check_password_hash

from clinic_app import db
from clinic_app.models.descriptors import DoctorUUID


class User(db.Model, UserMixin):
    """
    User object stands for representation of data row in `user` table.
    Table stores user information for authentication
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), nullable=False, unique=True, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'),
                          unique=True, index=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(127), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    last_modified = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow,
                              onupdate=datetime.utcnow)
    doctor = db.relationship('Doctor', back_populates='user', lazy='joined')
    doctor_uuid = DoctorUUID()

    def __init__(self, email: str, password_hash: str, is_admin: bool,
                 doctor_uuid: str = None) -> None:
        """
        :param email: email of user
        :param password_hash: user's password hash(of raw password if password_raw is set to True)
        :param is_admin: bool parameter for admins only, False by default
        :param doctor_uuid: uuid of related doctor
        """
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.uuid = str(uuid4())
        self.doctor_uuid = doctor_uuid

    def __repr__(self):
        return f'<User(email={self.email!r}, is_admin={self.is_admin}, uuid={self.uuid!r})>'

    def check_password(self, password: str) -> bool:
        """
        Check equality of given password with user's

        :param password: password to compare with employee's password
        :return: True if given password hash is equal to password hash of user
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """Get user's identifier for authorization"""
        return self.uuid
