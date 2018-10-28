@app.route('/blog', methods=['GET'])
def blog_list():
    
    if "user" in request.args:
        user_id = request.args.get("user")
        user = User.query.get(user_id)
        user_blogs = Blog.query.filter_by(owner=user).all()
        return render_template("singleUser.html", title= 'User Blogs', user_blogs=user_blogs)
    blogs = Blog.query.order_by(Blog.id.desc())
    return render_template('blog_list.html', title='Blog List', blogs=blogs )