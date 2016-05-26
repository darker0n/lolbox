from flask import Blueprint, render_template, request, redirect
from lolbox.models import *

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def homepage():
        posts = Post.objects.all()
        return render_template('index.html', posts=posts)

@home.route('/', methods=['POST'])
def new_post():
        text = request.form["text"]
        post = Post(text=text)
        post.save()
        return redirect(request.path)

@home.route('/rules')
def rules():
        return render_template('rules.html')
