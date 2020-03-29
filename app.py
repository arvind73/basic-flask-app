from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# sqlalchemy allows to interact w/ db like postres, sqlite, etc from flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
# __file__ is app.py
# where will data be stored, there is field called SQLALCHEMY_DATABSE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 3 slashes is relative path, 4 is absolute path(root directory). Create posts file
db = SQLAlchemy(app)  # link to database
''' Models structure the database. Think of database as table, each column as attribute. repr() prints represnts a database after its created'''


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author


# db.create_all()  # create all tables into database table
blog1 = BlogPost('post 1', 'science', 'Arvind')
blog2 = BlogPost('post 2', 'physics', 'Arnav')
# print(blog1.title)
# db.create_all()
# db.session.add_all([blog1, blog2])  # Now, the data stored to database
# db.session.commit()
# print(blog2.id)


@app.route('/')
def index():  # Browser can interpret anything from frunction, so add fuctionality to the return, it can also interpret html
    return render_template('index.html')


# Getting stuff from url, dynamic url, use it for ids, display images for those id.
# by default its only get request
@app.route('/home/<int:name>', methods=['GET'])
# It helps saving time, multiple urls for one function
def hello(name):
    return 'Welcome back ' + str(name)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':  # then read all data from form, send to db
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,
                            content=post_content, author=post_author)
        db.session.add(new_post)  # adds it to database in current session
        db.session.commit()  # saves it
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(
            BlogPost.date_created).all()  # get all of blogpost from db
        return render_template('posts.html', posts=all_posts)


@app.route('/home/users/<string:name>/posts/<int:id>')
@app.route('/posts/delete/<int:id>')
def delete(id):  # as id is unique
    # if it doesnt exist, it shouldnt break
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == "POST":
        flash('Posted success', 'info')
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        new_post = BlogPost(title=post_title,
                            content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    # get all data
    flash('Posted success' + request.method, 'info')
    if request.method == "POST":
        flash('Posted success', 'info')
        post.id = id
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


def all(name, id):
    return "hello, " + name + ", your id is " + str(id)


'''  In order to delete all rows
db.session.query(BlogPost).delete()
db.session.commit()
 '''

if __name__ == '__main__':
    app.run(debug=True)
