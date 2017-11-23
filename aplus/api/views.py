from flask import Flask, render_template, request, redirect, url_for, flash, \
	jsonify, Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy import or_


from aplus.models import db, PSSA, School

import random
import string

#from forms import CategoryForm, ItemForm
import re

api = Blueprint('api', __name__, template_folder="templates")


@api.route('/')
def index():
    """Prep category and item data then render the home page.

    Returns: Home page.
    """
    return render_template('index.html')


@api.route('/api/<year>/<school>/<grade>/<subject>/<subset>')
def apiPSSA(year, school, grade, subject, subset):
    score = PSSA.query.filter(PSSA.year==year).filter(PSSA.school==school)\
        .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
        .filter(PSSA.subset==subset).first()
    if score:
        resp = jsonify(score.serialize)
    else:
        return ('', 200)

    return resp


@api.route('/api/school/<school>/<year>/<grade>/<subject>/<subset>')
def apiSchoolPSSA(school, year, grade, subject, subset):
    if subject == "All" and subset != "All":
        scores = PSSA.query.filter(PSSA.year==year)\
            .filter(PSSA.school==school).filter(PSSA.grade==grade)\
            .filter(PSSA.subset==subset).all()
    elif subject != "All" and subset == "All":
        scores = PSSA.query.filter(PSSA.year==year)\
            .filter(PSSA.school==school).filter(PSSA.grade==grade)\
            .filter(PSSA.subject==subject).all()
    elif subject == "All" and subset == "All":
         scores = PSSA.query.filter(PSSA.year==year)\
            .filter(PSSA.school==school).filter(PSSA.grade==grade)\
            .filter(PSSA.subject==subject).all()
    else:
        scores = PSSA.query.filter(PSSA.year==year)\
            .filter(PSSA.school==school).filter(PSSA.grade==grade)\
            .filter(PSSA.subject==subject).filter(PSSA.subset==subset).all()
    if scores:
        print scores
        output = []
        for score in scores:
            output.append(score.serialize)
        resp = jsonify(data=output)
    else:
        return ('', 200)

    return resp

@api.route('/api/pssa/select/')
def menuSelectJSON():
    """API for browse select drop downs.

    Returns: JSON for all categories.
    """
    columns = ['year', 'school', 'subject', 'grade', 'subset']
    output = {}
    for col in columns:
        labels = db.session.query(getattr(PSSA,col))\
            .order_by(getattr(PSSA,col)).distinct().all()
        if labels:
            unzip = zip(*labels)
            output[col] = unzip
    print output
    resp = jsonify(output)
    resp.status_code = 200

    return resp


@api.route('/api/school/type/<school_type>')
def schoolTypeListJSON(school_type):
    """API for list of school by school type.
    Arguements: 
        school_type: string 'elementary', 'middle' or 'high' 

    Returns: JSON of a list schools of the given type.
    """
    if school_type == 'Elementary':
        configOpts = ['K-5', 'K-8']
    elif school_type == "Middle":
        configOpts = ['K-8', '6-8', '6-12']
    elif school_type == 'High':
        configOpts = ['6-12', '9-12']
    else:
        configOpts = []

    output = {}
    if configOpts != []:
        labels = db.session.query(School.school_name)\
            .filter(School.configuration.in_(configOpts))\
            .order_by(School.school_name).distinct().all()
        if labels:
            print labels
            unzip = zip(*labels)
            output['School'] = unzip
    resp = jsonify(output)
    resp.status_code = 200

    return resp


@api.route('/api/school/option/1/<school_name1>/2/<school_name2>')
def schoolOptJSON(school_name1, school_name2):
    """API for list of school by school type.
    Arguements: 
        school_name1: string of school name 1
        school_name2: string of school name 1

    Returns: JSON of a list schools of the given type.
    """
    columns = ['year', 'subject', 'grade', 'subset']
    output = {}
    for col in columns:
        labels = db.session.query(getattr(PSSA,col))\
            .filter(or_(PSSA.school==school_name1, PSSA.school==school_name2))\
            .order_by(getattr(PSSA,col)).distinct().all()
        if labels:
            unzip = zip(*labels)
            output[col] = unzip
    print output
    resp = jsonify(output)
    resp.status_code = 200

    return resp


