import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(250), unique=True)
    picture = db.Column(db.String(250))
    admin = db.Column(db.Boolean)

    def __init__(self, name, email, picture, admin):
        self.name = name
        self.email = email
        self.picture = picture
        self.admin = admin

    def __repr__(self):
        return '<Users %r>' % self.name


class PSSA(db.Model):
    year = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(250), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    grade = db.Column(db.String(250), nullable=False)
    subset = db.Column(db.String(250), nullable=False)
    total_tested = db.Column(db.Integer)
    below_basic = db.Column(db.Integer)
    basic = db.Column(db.Integer)
    proficient = db.Column(db.Integer)
    advanced = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, year, school, subject, grade, subset, total_tested,
        below_basic, basic, proficient, advanced):
        self.year = year
        self.school = school
        self.subject = subject
        self.grade = grade
        self.subset = subset
        self.total_tested = total_tested
        self.below_basic = below_basic
        self.basic = basic
        self.proficient = proficient
        self.advanced = advanced

    def __repr__(self):
        return '<PSSA Yr: {} Sch: {} Sbj: {} Gr: {} Set: {}>'.format(self.year,
            self.school, self.subject, self.grade, self.subset)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'year': self.year,
            'school': self.school,
            'subject': self.subject,
            'grade': self.grade,
            'subset': self.subset,
            'total_tested': self.total_tested,
            'below_basic': self.below_basic,
            'basic': self.basic,
            'proficient': self.proficient,
            'advanced': self.advanced
        }


class School(db.Model):
    school_name = db.Column(db.String(250), nullable=False)
    school_no = db.Column(db.String(250), nullable=False)
    configuration = db.Column(db.String(250), nullable=False)
    id = db.Column(db.Integer, primary_key=True)


    def __init__(self, school_name, school_no, configuration):
        self.school_name = school_name
        self.school_no = school_no
        self.configuration = configuration


    def __repr__(self):
        return '<School: {}>'.format(self.school_name)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'school_name': self.school_name,
            'school_no': self.school_no,
            'configuration': self.configuration
        }

