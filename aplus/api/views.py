from flask import Flask, render_template, request, redirect, url_for, flash, \
	jsonify, Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError


from aplus.models import db, PSSA

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



