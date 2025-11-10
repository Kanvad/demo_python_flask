from flask import Flask, request, make_response, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from dotenv import load_dotenv
import os
# from connect_db import db, init_db

# Load environment variables from .env file
load_dotenv()

# Create Flask application instance
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'

# Initialize database
# init_db(app)

@app.route('/')
def index():
    # """Homepage route"""
    # return '<h1>Hello World!</h1><p>Flask is working!</p>'
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, {}!</h1>'.format(name)
    return render_template('user.html', name=name)


@app.route('/about')
def about():
    # """About page route"""
    # return '<h1>About</h1><p>This is a Flask application.</p>'
    return render_template('about.html')


@app.route('/info')
def info():
    user_agent = request.headers.get('User-Agent')
    return '''
    <h2>Request Information</h2>
    <p><strong>Method:</strong> {}</p>
    <p><strong>URL:</strong> {}</p>
    <p><strong>User-Agent:</strong> {}</p>
    <p><strong>Remote IP:</strong> {}</p>
    '''.format(request.method, request.url, user_agent, request.remote_addr)

@app.route('/variables/<name>')
def variables_demo(name):
    user_data = {
        'email': f'{name.lower()}@example.com',
        'age': 25
    }
    hobbies = ['reading', 'programming', 'music']
    
    return render_template('variables_demo.html', 
                         name=name, 
                         user_data=user_data, 
                         hobbies=hobbies)
    
@app.route('/conditionals')
def conditionals():
    user = {
        'name': 'Admin User',
        'is_admin': True
    }
    return render_template('conditionals.html', user=user)

@app.route('/loops')
def loops():
    users = [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'},
        {'name': 'Charlie', 'email': 'charlie@example.com'}
    ]
    return render_template('loops.html', users=users)

@app.route('/bad')
def bad_request():
    return '<h1>Bad Request</h1>', 400

@app.route('/not-found') 
def not_found():
    return '<h1>Page Not Found</h1>', 404

@app.route('/cookie')
def set_cookie():
    response = make_response('<h1>Cookie has been set!</h1>')
    response.set_cookie('username', 'flask_user')
    return response

@app.route('/redirect-test')
def redirect_test():
    return redirect(url_for('index'))

# bootstrap
@app.route('/bootstrap/user/<name>')
def bootstrap_user(name):
    return render_template('bootstrap_user.html', name=name)

@app.route('/datetime')
def datetime_demo():
    return render_template('datetime_demo.html', current_time=datetime.utcnow())

# error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Test route to trigger 500 error
@app.route('/error500')
def error500():
    # Intentionally cause an error
    return 1 / 0

if __name__ == '__main__':
    # Run development server
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
    