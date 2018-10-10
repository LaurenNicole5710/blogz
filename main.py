from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

blogs = Blog.query.all()

@app.route('/')
def blog_list():
    return render_template('blog_list.html', title='Blog List', blogs=blogs )

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()   
    return render_template('newpost.html', title="New Post")


@app.route('/blog_id', methods=['POST'])
def blog_id():
    blog_id = request.form['blog_id']
    blog = Blog.query.get(blog_id)
    return render_template('blog_id.html', title="Your Entry", blog=blog)

if __name__ == '__main__':
    app.run()
