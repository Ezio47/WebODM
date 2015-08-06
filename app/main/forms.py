from flask.ext.wtf import Form
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class NewSequenceForm(Form):
    label = StringField("Label", validators=[Required()])
    photos = FileField("Photos", validators=[Required()]) #, Regexp('^.*\.(jpg)$',0,'Filetype must be \'.jpg\'')])
    submit = SubmitField("Submit")
