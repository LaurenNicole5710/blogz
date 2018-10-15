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

@app.route('/blog')
def blog_list():
    blogs = Blog.query.all()
    return render_template('blog_list.html', title='Blog List', blogs=blogs )

@app.route('/newpost', methods=['GET'])
def newpost():
    blog_title = request.args.get('title')
    blog_body = request.args.get('body')
    new_blog = Blog(blog_title, blog_body)
    db.session.add(new_blog)
    db.session.commit()  
    #if blog_title != ' ' or blog_body != ' ':
        #return redirect('/blog_id')
    #else: 
        # TODO - flash message
        #return 'ERROR'
    return render_template('newpost.html', title="New Post")

@app.route('/blog_id', methods=['GET'])
def blog_id():
    blog = request.args.get('blog_id')
    blog = Blog.query.get(blog)
    return render_template('blog_id.html', title="Your Entry", blog=blog)

if __name__ == '__main__':
    app.run()