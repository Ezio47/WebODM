from datetime import datetime
import os
from flask import render_template, session, request, redirect, url_for, current_app, send_file
from . import main
from .. import db
from ..models import User, Sequence, Photo
from flask.ext.login import login_required, current_user
from flask.ext.uploads import UploadSet
from werkzeug import secure_filename
from ..decorators import admin_required, permission_required
from PIL import Image
import shutil

# Home Page
@main.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_anonymous():
        sequences = Sequence.query.filter_by(user_id=current_user.id)
        return render_template('index.html', sequences=sequences)
    return render_template('index.html')

# User Page
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        abort(404)
    return render_template('user.html',user=user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# New sequence
@main.route('/new', methods=['GET','POST'])
@login_required
def new():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    username = current_user.username
    label = request.form.get('label')
    # if this sequence name doesn't exist 
    if label is not None and not Sequence.query.filter_by(label=label, user_id=current_user.id).first():
        sequence = Sequence(label = label, user = current_user._get_current_object())
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload folder we setup
                #make user folder
                directory = current_app.config['UPLOAD_DEFAULT_DEST'] + username + '/' + label + '/' 
                if not os.path.exists(directory):
                    os.makedirs(directory + 'thumbs/')
                file.save(directory + filename)
                #create a thumbnail
                image = Image.open(directory + filename)
                image.thumbnail((158,116), Image.ANTIALIAS)
                image.save(directory + 'thumbs/' + filename, 'JPEG', quality=88)
                # Save the filename into a list, we'll use it later
                filenames.append(filename)
                #add photo to the database
                photo = Photo(file=filename, sequence = sequence)
                db.session.add(photo)
        db.session.add(sequence)
        db.session.commit()
        return redirect(url_for('.sequence', label = sequence.label, user=username))
    return render_template('new_sequence.html', filenames=filenames)

@main.route('/sequence/<user>/<label>', methods=['GET'])
@login_required
def sequence(user, label):
# check if label exists, otherwise go to error sequence not found page
    if label == None:
        abort(404)
    seq = Sequence.query.filter_by(label=label).first()
    photos = Photo.query.filter_by(sequence_id=seq.id).all() 
    return render_template('sequence.html', label=label, user=user, sequence=seq, photos=photos)

@main.route('/photo/<user>/<label>/<file>', methods=['GET'])
@login_required
def photo(user, label, file):
    if id == None:
        abort(404)
    photo = Photo.query.filter_by(file=file).first()
    filedir = current_app.config['UPLOAD_DEFAULT_DEST'] + user + '/' + label + '/' + photo.file
    return send_file(filedir, mimetype='image/jpg')

@main.route('/thumbnail/<user>/<label>/<file>', methods=['GET'])
@login_required
def thumbnail(user, label, file):
    if id == None:
        abort(404)
    photo = Photo.query.filter_by(file=file).first()
    filedir = current_app.config['UPLOAD_DEFAULT_DEST'] + user + '/' + label + '/thumbs/' + photo.file
    return send_file(filedir, mimetype='image/jpg')

@main.route('/sequence/<user>/<label>/delete', methods=['GET','POST'])
@login_required
def delete(user, label):
    this_user = User.query.filter_by(username=user).first()
    sequence = Sequence.query.filter_by(user_id=this_user.id, label=label).first()
    # delete the directory containing the photos
    if sequence is not None:
        db.session.delete(sequence)
        db.session.commit()
        directory = current_app.config['UPLOAD_DEFAULT_DEST'] + user + '/' + label + '/'
        shutil.rmtree(directory)
    	return redirect(url_for('.index'))
    
    return redirect(url_for('.sequence', label=sequence.label, user=sequence.user))
