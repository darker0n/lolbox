from flask import Blueprint, render_template, request, redirect
from lolbox.models import *
from flask.ext.login import login_required, current_user

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
@login_required
def index():
        posts = Post.objects.all()
        return render_template('index.html', posts=posts)

@home.route('/', methods=['POST'])
@login_required
def new_post():
        text = request.form["text"]
        post = Post(text=text, author=str(current_user.id))
        post.save()
        return redirect(request.path)

@home.route('/rules')
def rules():
        return render_template('rules.html')
