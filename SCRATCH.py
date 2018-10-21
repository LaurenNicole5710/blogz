from flask import Flask, request, redirect, render_template, url_for
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

blog_id = Blog.id

@app.route('/blog')
def blog_list():
    blogs = Blog.query.all()
    return render_template('blog_list.html', title='Blog List', blogs=blogs )

@app.route('/post/blog_id')
def post(blog_id):
    blog = Blog.query.get(id=blog_id).one()
    return render_template('blog_id.html', blog=blog)



@app.route('/add', methods=['GET', 'POST'])
def add_post():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    
    title = request.form['title']
    body = request.form['body']
    
    new_blog = Blog(title=title, body=body)

    if title == '':
        error = "Please fill in a title."
    elif body == '':
        error = "Please make a post."
    
    db.session.add(new_blog)
    db.session.commit()  


    return render_template('blog_id.html', title=title, body=body)

def newpost():
    blog_title = request.form['title']
    blog_body = request.form['body']
    
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