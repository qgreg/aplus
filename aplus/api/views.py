from __future__ import division
from flask import Flask, render_template, request, redirect, url_for, flash, \
	jsonify, Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy import or_, func

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
    race = [
      "American Indian or Alaska Native",
      "Asian",
      "Black",
      "Hispanic",
      "Multi-Racial",
      "Native Hawaiian or Other Pacific Islander",
      "White"
    ]
    if school == "All" and subset != "All":
        score = db.session.query(
            func.sum(PSSA.proficient).label("proficient"),
            func.sum(PSSA.advanced).label("advanced"),
            func.sum(PSSA.basic).label("basic"),
            func.sum(PSSA.below_basic).label("below_basic"), 
            func.sum(PSSA.total_tested).label('total_tested'),
            PSSA.year, PSSA.grade, PSSA.subset, PSSA.subject)\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.subject)\
            .group_by(PSSA.subset)\
            .filter(PSSA.year==year)\
            .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
            .filter(PSSA.subset==subset).first()
    elif school != "All" and subset == "All":
        score = db.session.query(
            func.sum(PSSA.proficient).label("proficient"),
            func.sum(PSSA.advanced).label("advanced"),
            func.sum(PSSA.basic).label("basic"),
            func.sum(PSSA.below_basic).label("below_basic"), 
            func.sum(PSSA.total_tested).label("total_tested"),
            PSSA.year, PSSA.grade, PSSA.school, PSSA.subject)\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.subject)\
            .group_by(PSSA.school)\
            .filter(PSSA.year==year).filter(PSSA.school==school)\
            .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
            .filter(PSSA.subset.in_(race)).first()
    elif school == "All" and subset == "All":
        score = db.session.query(
            func.sum(PSSA.proficient).label('proficient'),
            func.sum(PSSA.advanced).label('advanced'),
            func.sum(PSSA.basic).label('basic'),
            func.sum(PSSA.below_basic).label('below_basic'), 
            func.sum(PSSA.total_tested).label('total_tested'),
            PSSA.year, PSSA.grade, PSSA.subject)\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.subject)\
            .filter(PSSA.year==year)\
            .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
            .filter(PSSA.subset.in_(race)).first()
    else:
        score = PSSA.query.filter(PSSA.year==year).filter(PSSA.school==school)\
            .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
            .filter(PSSA.subset==subset).first()
    if score:
        score.school = school
        score.subset = subset
        if score.total_tested < 11:
            resp = jsonify({
                'year': score.year,
                'school': score.school,
                'subject': score.subject,
                'grade': score.grade,
                'subset': score.subset,
                'total_tested': score.total_tested,
                'status': 'Data hidden to protect student privacy.'})
        else:
            resp = jsonify({
                'year': score.year,
                'school': score.school,
                'subject': score.subject,
                'grade': score.grade,
                'subset': score.subset,
                'total_tested': score.total_tested,
                'proficient': score.proficient,
                'advanced': score.advanced,
                'below_basic': score.below_basic,
                'basic': score.basic})
    else:
        return ('', 200)

    return resp


@api.route('/api/list/<year>/<grade>/<subject>/<subset>')
def apiListPSSA(year, grade, subject, subset):
    scores = PSSA.query.filter(PSSA.year==year)\
        .filter(PSSA.grade==grade).filter(PSSA.subject==subject)\
        .filter(PSSA.subset==subset).all()
    if scores:
        output = []
        for score in scores:
            ts = score.serialize
            if 'total_tested' in ts:
                if score.total_tested < 11:
                    ts = {
                        'year': score.year,
                        'school': score.school,
                        'subject': score.subject,
                        'grade': score.grade,
                        'subset': score.subset,
                        'total_tested': score.total_tested,
                        'status': 'Data hidden to protect student privacy.'}
                else:
                    if 'below_basic' in ts:
                        ts['below_basic_rate'] = round(float(ts['below_basic']/
                            ts['total_tested']*100),1)
                    if 'basic' in ts:
                        ts['basic_rate'] = round(float(
                            ts['basic']/ts['total_tested']*100),1)
                    if 'proficient' in ts:
                        ts['proficient_rate'] = round(float(
                            ts['proficient']/ts['total_tested']*100),1)
                    if 'advanced' in ts:
                        ts['advanced_rate'] = round(float(
                            ts['advanced']/ts['total_tested']*100),1)
            output.append(ts)
        resp = jsonify(data=output)
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
            .filter(PSSA.school==school).filter(PSSA.grade==grade).all()
    else:
        scores = PSSA.query.filter(PSSA.year==year)\
            .filter(PSSA.school==school).filter(PSSA.grade==grade)\
            .filter(PSSA.subject==subject).filter(PSSA.subset==subset).all()
    if scores:
        output = []
        for score in scores:
            ts = score.serialize
            if hasattr(score, 'total_tested'):
                if score.total_tested < 11:
                    ts = {
                        'year': score.year,
                        'school': score.school,
                        'subject': score.subject,
                        'grade': score.grade,
                        'subset': score.subset,
                        'total_tested': score.total_tested,
                        'status': 'Data hidden to protect student privacy.'}
            output.append(ts)
        resp = jsonify(data=output)
    else:
        return ('Nothing', 200)

    return resp


@api.route('/api/3rdELA/<year>/<school>/<subset>')
def api3rdELA(year, school, subset):
    if school == "All" and subset == "All":
        result = db.session.query(PSSA.year, PSSA.grade, 
            (func.sum(PSSA.proficient) + func.sum(PSSA.advanced)).label(
                "grade_level"),
            (func.sum(PSSA.total_tested).label("total_tested")))\
            .group_by(PSSA.year).group_by(PSSA.grade)\
            .filter(PSSA.year==year).filter(PSSA.grade=="3rd").first()
    elif school != "All" and subset == "All":
        result = db.session.query(PSSA.year,  PSSA.grade, PSSA.school, 
            (func.sum(PSSA.proficient) + func.sum(PSSA.advanced)).label(
                "grade_level"),
            (func.sum(PSSA.total_tested).label("total_tested")))\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.school)\
            .filter(PSSA.year==year).filter(PSSA.grade=="3rd")\
            .filter(PSSA.school==school).first()
    elif school == "All" and subset != "All":
        result = db.session.query(PSSA.year,  PSSA.grade, PSSA.subset, 
            (func.sum(PSSA.proficient) + func.sum(PSSA.advanced)).label(
                "grade_level"),
            (func.sum(PSSA.total_tested).label("total_tested")))\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.subset)\
            .filter(PSSA.year==year).filter(PSSA.grade=="3rd")\
            .filter(PSSA.subset==subset).first()
    else:
        result = db.session.query(PSSA.year, PSSA.grade, PSSA.school, 
            PSSA.subset, (func.sum(PSSA.proficient) + func.sum(
                PSSA.advanced)).label("grade_level"),
            (func.sum(PSSA.total_tested).label("total_tested")))\
            .group_by(PSSA.year).group_by(PSSA.grade).group_by(PSSA.school)\
            .group_by(PSSA.subset)\
            .filter(PSSA.year==year).filter(PSSA.grade=="3rd")\
            .filter(PSSA.school==school).filter(PSSA.subset==subset).first()
    if result:
        print (result)
        if result.total_tested < 11:
            result['grade_level'] = ''
            result['status'] = 'Data hidden to protect student privacy.'
        resp = jsonify(data=result)
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


@api.route('/api/third/select/')
def thirdMenuSelectJSON():
    """API for browse third grade select drop downs.

    Returns: JSON for all categories.
    """
    columns = ['school', 'subset']
    output = {}
    for col in columns:
        labels = db.session.query(getattr(PSSA,col))\
            .filter(PSSA.grade=="3rd").filter(PSSA.year=="2017")\
            .filter(PSSA.subject=="PSSA ELA")\
            .order_by(getattr(PSSA,col)).distinct().all()
        if labels:
            unzip = zip(*labels)
            output[col] = unzip
    print output
    resp = jsonify(output)
    resp.status_code = 200

    return resp


@api.route('/api/pssa/list/<school_type>')
def schoolTypeListJSON(school_type):
    """API for list options for drop down filtered for school type.
    Arguements: 
        school_type: string 'elementary', 'middle' or 'high' 

    Returns: JSON for columns and options.
    """
    if school_type == 'Elementary':
        grades = ['3rd', '4th', '5th']
    elif school_type == "Middle":
        grades = ['6th', '7th', '8th']
    elif school_type == 'High':
        grades = ['9th', '10th', '11th', '12th']
    else:
        grades = []

    columns = ['year', 'subject', 'grade', 'subset']
    output = {}
    if grades != []:
        for col in columns:
            labels = db.session.query(getattr(PSSA,col))\
                .filter(PSSA.grade.in_(grades))\
                .order_by(getattr(PSSA,col)).distinct().all()
            if labels:
                unzip = zip(*labels)
                output[col] = unzip
    print output
    resp = jsonify(output)
    resp.status_code = 200

    return resp


@api.route('/api/school/type/<school_type>')
def schoolTypeJSON(school_type):
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


