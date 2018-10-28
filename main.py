from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.blogs = blogs

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', '/', 'newpost']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    user_list = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', user_list=user_list)

@app.route('/blog', methods=['GET'])
def blog_list():
    if "user" in request.args:
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        user_blogs = Blog.query.filter_by(owner=user).all()
        return render_template("singleUser.html", title= 'User Blogs', user_blogs=user_blogs)
    
    if "id" in request.args:
        id = request.args.get("id")
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog_id.html', title="Your Entry", blog=blog)
    
    blogs = Blog.query.order_by(Blog.id.desc())
    return render_template('blog_list.html', title='Blog List', blogs=blogs )

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error = ''
    body_error = ''
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_body, blog_owner)
    
        if new_blog.title == '':
            title_error = "Please enter a title."
            blog_title = ''
        if new_blog.body == '':
            body_error = "Please enter blog content."
            blog_body = ''
       
        if not title_error and not body_error:
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/blog?id=' + str(new_blog.id))
        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
    return render_template('newpost.html')

#@app.route('/blog_id', methods=['GET'])
#def blog_id():
    #id = request.args.get('id')
    #blog = Blog.query.filter_by(id=id).first()
    #return render_template('blog_id.html', title="Your Entry", blog=blog)



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_error = ''
    password_error = ''
    verify_error = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if username == '':
            username_error = "Please enter a username."
        elif ' ' in username:
            username_error = "Username may not contain any spaces."
            username = ''
        elif len(username) < 3 or len(username)> 20: 
            username_error = "Please enter a username between 3 and 20 characters."
            username = ''
        
        if password == '':
            password_error = "Please enter a password."
        elif (len(password)) <3 or (len(password))> 20:
            password_error = "Please enter a password between 3 and 20 characters"
            
        if verify == '':
            verify_error = "Please confirm your password."
        elif password != verify:
            verify_error = "Passwords do not match."

        if not username_error and not password_error and not verify_error:

            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
            # TODO - user better response messaging
                return "<h1>Duplicate user</h1>"
    return render_template('signup.html', username_error=username_error, password_error=password_error, verify_error=verify_error)

    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()