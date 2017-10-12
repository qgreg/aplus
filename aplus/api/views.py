from flask import Flask, render_template, request, redirect, url_for, flash, \
	jsonify, Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError


from models import db, PSSA

import random
import string

#from forms import CategoryForm, ItemForm
import re

api = Blueprint('api', __name__, template_folder="templates")


@category.route('/')
def index():
    """Prep category and item data then render the home page.

    Returns: Home page.
    """
    return render_template('index.html')


@category.route('/category/JSON')
def categoriesJSON():
    """API for all categories.

    Returns: JSON for all categories.
    """
    categories = Category.query.all()
    return jsonify(CAtegory=[i.serialize for i in categories])

