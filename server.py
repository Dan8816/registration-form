from flask import Flask, render_template, request, redirect, session, flash, url_for
import re
from datetime import datetime, date, time
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


app = Flask(__name__)
app.secret_key = 'ThisIsSecret'


def validaShuns():
    errors = 0
    #first name
    if request.form['firstName'] == '':
        flash('No name, no pass!', 'firstNameError')
        errors += 1
        pass
    elif any(char.isdigit() for char in request.form['firstName']) == True:
        flash('Who puts numbers in their name', 'firstNameError')
        errors += 1
        pass
    else:
        session['firstName'] = request.form['firstName']
    #Check last name
    if request.form['lastName'] == '':
        flash('Ahh whats the matter? no family!', 'lastNameError')
        errors += 1
        pass
    elif any(char.isdigit() for char in request.form['lastName']) == True:
        flash('Who puts numbers in their name', 'lastNameError')
        errors += 1
        pass
    else:
        session['lastName'] = request.form['lastName']
    #Check email
    if request.form['email'] == '':
        flash('Gimme an email', 'emailError')
        errors += 1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('You born under a rock, 1980 called!', 'emailError')
        errors += 1
        pass
    else:
        session['email'] = request.form['email']
    #Check password
    if request.form['password'] == '':
        flash('Yes, password bub!', 'passwordError')
        errors += 1
        pass
    elif len(request.form['password']) < 8:
        flash('Your password is too easy', 'passwordError')
        errors += 1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password needs at least 1 little letter, 1 capital letter, and 1 number', 'passwordError')
    else:
        session['password'] = request.form['password']
    #Check confirmation password
    if request.form['confirmPassword'] == '':
        flash('Yes, that password goes here also', 'confirmPasswordError')
        errors += 1
        pass
    elif request.form['confirmPassword'] != request.form['password']:
        flash('Double check that password, Jeesh!!!!', 'confirmPasswordError')
        errors += 1
    else:
        session['confirmPassword'] = request.form['confirmPassword']
    #See if there are any errors
    if errors > 0:
        session['password'] = ''
        session['confirmPassword'] = ''
        return False
    else:
        return True


@app.route('/')
def index():
    if 'firstName' not in session:
        session['firstName'] = ''
    if 'lastName' not in session:
        session['lastName'] = ''
    if 'email' not in session:
        session['email'] = ''
    if 'password' not in session:
        session['password'] = ''
    if 'confirmPassword' not in session:
        session['confirmPassword'] = ''

    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    if validaShuns() == False:
        return redirect('/')
    return redirect('/process')

@app.route('/process')
def youPass():
    return render_template('results.html')

@app.route('/clear', methods=['POST'])
def clear():
    session['firstName'] = ''
    session['lastName'] = ''
    session['email'] = ''
    session['password'] = ''
    session['confirmPassword'] = ''

    return redirect('/')

app.run(debug=True)
