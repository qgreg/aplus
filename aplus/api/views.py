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


@api.route('/api/2016/ELA/Phillips')
def apiPSSA():
    return jsonify(
        year=2016,
        school='Phillips',
        subject='ELA',
        grade='3rd',
        subset='All',
        total_tested=45,
        below_basic=0.067,
        basic=0.356,
        proficient=0.467,
        advanced=0.111)


#@api.route('/category/JSON')
#def categoriesJSON():
    """API for all categories.

    Returns: JSON for all categories.
    """
    # categories = Category.query.all()
    #return jsonify(Category=[i.serialize for i in categories])

