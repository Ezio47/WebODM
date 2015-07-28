from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
#from .forms import NameForm
from .. import db
from ..models import User
from flask.ext.login import login_required
# Home Page
@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

# User Page
@main.route('/user/<name>')
@login_required
def user(name):
	return render_template('user.html',name=name)
