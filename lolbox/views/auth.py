# coding: utf-8

from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from lolbox.models import *
from flask.ext.login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET'])
def signin():
    return render_template('auth/signin.html')

@auth.route('/signin', methods=['POST'])
def login():
    password = request.form["password"]
    email = request.form["email"]
    user = User.objects.get(email=email)
    remember_me = False
    if 'remember' in request.form:
        remember_me = True
    if user is not None and user.verify_password(password, user.password):
        login_user(user, remember_me)
        return redirect(url_for('home.index'))

    flash(u"Неверный Email или пароль.")
    return render_template('auth/signin.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
