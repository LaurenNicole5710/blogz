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
            flash("Please enter a title.", "error")
        
        if new_blog.body == '':
            flash("Please enter blog content.", "error")
       
        if new_blog.title != '' and new_blog.body != '':
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/blog?id=' + str(new_blog.id))
        else:
            return render_template('newpost.html')
    return render_template('newpost.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if username == '':
            flash("Please enter a username.", "error")
        if len(username) < 3: 
            flash("Please enter a username greater than 3 characters.", "error")
        
        if password == '':
            flash("Please enter a password.", "error")
        if (len(password)) <3:
            flash("Please enter a password greater than 3 characters.", "error")
        
        if verify == '':
            flash("Please confirm your password.", "error")
        if password != verify:
            flash("Passwords do not match.", "error")

            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                flash("User already exists.")
    return render_template('signup.html')

    

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
        if user and user.password != password:
            flash('User password incorrect.', 'error')
        else:
            flash('User does not exist.', 'error')

    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()