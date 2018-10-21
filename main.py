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


@app.route('/')
def blog_list():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog_list.html', title='Blog List', blogs=blogs )

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ''
    body_error = ''
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
    
        if blog_title == '':
            title_error = "Please enter a title."
            blog_title = ''
        elif blog_body == '':
            body_error = "Please enter blog content."
            blog_body = ''
       
        if blog_title or blog_body != '':
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/blog_id?id=' + str(new_blog.id))
    else:
        return render_template('newpost.html', title_error=title_error, body_error=body_error)

@app.route('/blog_id', methods=['GET'])
def blog_id():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    return render_template('blog_id.html', title="Your Entry", blog=blog)

if __name__ == '__main__':
    app.run()