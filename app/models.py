from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
import enum

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class NaGroup(db.Model):
    """
    Create a GroupTable
    """

    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    info_link = db.Column(db.String(200), unique=False)
    address = db.Column(db.String(200), unique=False)
    description = db.Column(db.String(255), unique=False)
    last_update = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    ya_geo_link = db.Column(db.String(300), unique=False)
    group_type = db.Column(db.String(10))

    def __repr__(self):
        return '<Group: {}>'.format(self)

class ParsingLog(db.Model):
    """
    Create parsingLog table
    """
    __tablename__ = 'parsinglog'
    id = db.Column(db.Integer, primary_key=True)
    source_link = db.Column(db.String(255), unique=False)
    file_link = db.Column(db.String(255), unique=False)
    last_update = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    parcing_status = db.Column(db.String(10), unique=False)

class ParsingStatus(enum.Enum):
    PROJECT = 'Project'
    INPROCESS = 'In process'
    COMPLITE = 'Complite'
    DECLINED = 'Declined'
    CLEARED = 'Cleared'

class ParsingType(enum.Enum):
    AA = 'AA'
    NA = 'NA'
    BOTH = 'AA+NA'

class ParsingTask(db.Model):
    """
    Parsing task to track and perform task
    """
    __tablename__ = 'parsingtask'
    guid = db.Column(db.String(36), primary_key=True)
    source_link = db.Column(db.String(255), nullable=False)
    target_file = db.Column(db.String(255), nullable=False)
    parsing_status = db.Column(db.Enum(ParsingStatus,
                                            values_callable=lambda x: [str(e.value) for e in ParsingStatus]),
                               nullable=False)
    parsing_type = db.Column(db.Enum(ParsingType,
                                     values_callable=lambda x: [str(e.value) for e in ParsingType]),
                             nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)