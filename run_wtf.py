from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, SelectField, 
                     BooleanField, PasswordField, IntegerField)
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, ValidationError
from werkzeug.utils import secure_filename
import os
import time
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-string-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Tạo thư mục uploads
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Custom validator
def vietnamese_phone_check(form, field):
    phone_pattern = r'^(0[3|5|7|8|9])+([0-9]{8})'
    if not re.match(phone_pattern, field.data):
        raise ValidationError('Please enter a valid Vietnamese phone number.')

# Form classes
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('sales', 'Sales Question'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(10, 500)])
    newsletter = BooleanField('Subscribe to newsletter')
    submit = SubmitField('Send Message')

class PhotoUploadForm(FlaskForm):
    photo = FileField('Upload Photo', validators=[
        FileRequired('Please select a file'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    title = StringField('Photo Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Upload Photo')

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index2.html', form=form, name=session.get('name'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Thank you {form.name.data}! Your message has been sent.')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    form = PhotoUploadForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        
        # Thêm timestamp
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(time.time())}{ext}"
        
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        
        flash(f'Photo "{form.title.data}" uploaded successfully!')
        return redirect(url_for('upload_photo'))
    
    return render_template('upload.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)