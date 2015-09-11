from flask import render_template, redirect, url_for, request, Response
import json
from blog import app
from .database import session
from .models import Post, Comment, User
import mistune
import datetime
from flask import flash
from flask.ext.login import login_user, login_required,current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.mail import Mail, Message


@app.route("/post")
@app.route("/page/<int:page>")
@login_required
def posts(page=1, paginate_by=5):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]
    admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        admin = admin
    )

@app.route("/")
def main():
    return redirect(url_for("login_get"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    flash("You have logged in", "info")
    return redirect(request.args.get('next') or url_for("posts"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login_get'))



@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")
    

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    members = session.query(User).all()
    post = Post(
        title=request.form["title"],
        content=request.form["content"],
        description = request.form["description"],
        author=current_user
    )
    session.add(post)
    session.commit()
    all_members = []
    for member in members:
        all_members.append(member.email)
    all_members = [str(i) for i in all_members]
    describe = request.form["description"] +".... View full message on TeamForum!"
    mail=Mail(app) 
    with mail.connect() as conn:
      for email in all_members:
        message = Message(subject="A new forum has been created by "+ current_user.name,
                  body= describe,
                  sender=("TeamForum", "kesfrance@gmail.com"),
                  recipients=[email]
                 )

        conn.send(message)

    flash("You have created a new forum. Team members have been notified.", "info")
    return redirect(url_for("posts"))    

#view for single post
@app.route("/post/<int:id>", methods=['GET'])
def singlepost_get(id):
    try:
        post = session.query(Post).filter_by(id=id).one()    
        comments = session.query(Comment).filter_by(post_id=post.id)
        comments = comments.order_by(Comment.datetime.desc()).all()
        admin = session.query(User).filter_by(email="kesfrance@yahoo.com").one()
    
        return render_template("singlepost.html",
                           post=post, 
                           id=id, 
                           comments=comments,
                           admin = admin                          
                          )
    except:
          error_msg = "Sorry, the page you are trying to view doesn't exist."
          return render_template("error.html",error_msg=error_msg)

@app.route("/post/<int:id>", methods= ['POST'])
@login_required
def singlepost_comment(id):
    post = session.query(Post).filter_by(id=id).one()
    comments = session.query(Comment).filter_by(post_id=post.id).all() 
    
    #mail list of people who commented on a forum, dont include comment author
    participants = list(set([str(i.author.email) for i in comments
                            if i.author.email != current_user.email]))
    
    #if the current user is not the creator of forum, add forum creator to list
    if post.author.email != current_user.email:
        participants.append(str(post.author.email))   
    
    content = request.form["content"][:30] + "....View full message on TeamForum."
    
    comment = Comment(
        post=session.query(Post).get(id),
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(comment)
    session.commit()
    
    if len(participants) != 0:
      mail=Mail(app) 
      with mail.connect() as conn:
          for email in list(set(participants)):
            message = Message(subject= current_user.name + " made a comment on "            
                  + post.title, body= content,
                  sender=("TeamForum", "kesfrance@gmail.com"),
                  recipients=[email]
                 )

            conn.send(message)

    flash("You've posted a comment. Paricipants will be notified", "info")
  
    return redirect(url_for("singlepost_get", id=id))

@app.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])       
def editComment(comment_id):
    commentToEdit= session.query(Comment).filter_by(id=comment_id).one()
    if request.method == 'POST':
        if request.form['content']:
            commentToEdit.content = request.form['content']
            commentToEdit.datetime = datetime.datetime.now()
            session.add(commentToEdit)
            session.commit()
        flash("You have editted your comment", "info")
        return redirect(url_for('posts'))
    else:
        return render_template('editcomment .html', p=commentToEdit)
        
@app.route("/comment/<int:comment_id>/delete", methods=['GET', 'POST'])       
def deleteComment(comment_id):
    commentToDelete = session.query(Comment).filter_by(id=comment_id).one()
    if request.method == 'POST':
        session.delete(commentToDelete)
        session.commit()
        flash("You have deleted your comment", "info")
        return redirect(url_for('posts'))
    else:       
        return render_template('deletecomment.html', i=commentToDelete)
        
        
@app.route("/post/<int:id>/edit", methods=['GET', 'POST'])
def editpost(id):
    postToEdit= session.query(Post).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['title']:
            postToEdit.title = request.form['title']
            postToEdit.content = request.form['content']
            postToEdit.datetime = datetime.datetime.now()
            session.add(postToEdit)
            session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template('editpost.html', p=postToEdit)
    
@app.route("/post/<int:id>/delete", methods = ["GET", "POST"])
def deletepost(id):
    postToDelete = session.query(Post).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(postToDelete)
        session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template('deletepost.html', i=postToDelete)
        

@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    password_2=request.form["re-password"]
    
    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("signup_get"))
        
    if not (password and password_2) or password != password_2:
        flash("Passwords did not match", "danger")
        return redirect(url_for("signup_get"))
    
    user = User(name=name, email=email, password=generate_password_hash(password))
    
    session.add(user)
    session.commit()
    
    flash("Success! You may now login with your credentials", "info")
    return redirect(url_for("login_get"))


@app.route("/post/JSON", methods=["GET"])
def posts_get():
    """ Get a list of posts """
    posts = session.query(Post).order_by(Post.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/post/<int:id>/JSON", methods=["GET"])
def post_get(id):
    """ Single post endpoint """
    post = session.query(Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
