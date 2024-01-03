import os
import secrets
import random
import string
from flask_mail import Mail, Message
from flask import Flask, render_template, request, flash, redirect, abort, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import Image
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '1c4aeea2b6d72bec641d737589e99665'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///share.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'assist.shareit@gmail.com'
app.config['MAIL_PASSWORD'] = 'atnu gvmw zwly vegf'

db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_image = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(15), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.image})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.date}, {self.content})"


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():

    return render_template('home.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profiles', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Image()
    if current_user.is_authenticated:
        return redirect(url_for('feeds'))
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            hsh_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user_conf = User.query.filter_by(username=request.form['username']).first()
            user_conf_email = User.query.filter_by(email=request.form['email']).first()
            if user_conf or user_conf_email:
                flash('Username or Email exists.Pick another', 'danger')
            else:
                image = save_picture(form.image.data)
                new_user = User(username=request.form['username'], email=request.form['email'], user_image=image,
                                password=hsh_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registered Successful, Login to share your experiences', 'success')
                return redirect(url_for('login'))
        else:
            flash('Passwords Do not match', 'danger')

    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feeds'))

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash('Login Successful, Welcome back', 'success')
            return redirect(url_for('feeds'))
        else:
            flash("Incorrect Email or Password", 'danger')

    return render_template('login.html', title='login')


@app.route('/feeds', methods=['GET'])
def feeds():
    feed = Post.query.order_by(Post.id.desc()).all()

    return render_template('feeds.html', title='Feeds', posts=feed)


@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    if request.method == 'POST':
        new_post = Post(title=request.form['title'], content=request.form['content'], author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Experience  Shared', 'success')
        return redirect(url_for('feeds'))

    return render_template('post.html', title='New Share')


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    posts = Post.query.filter_by(author=current_user).order_by(Post.date.desc())
    image_file = url_for('static', filename='profiles/' + current_user.user_image)

    return render_template('account.html', title='Account', image_file=image_file, posts=posts)


@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def feed(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('feed.html', title=f'{post.author.username}/{post.title}', post=post)


@app.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Experience Deleted", 'success')
    return redirect(url_for('account'))


def get_code(user):
    characters = string.digits
    code = ''.join(random.choice(characters) for _ in range(6))
    msg = Message('Password Reset Request', sender='noreply@app.com', recipients=[user.email])
    msg_body = f"""Dear {user.username} 
    Your reset code is {code}
    """
    data = {
        'app_name': 'SHARE IT',
        'title': 'Password Reset',
        'body': msg_body
    }
    msg.html = render_template('email.html', data=data)
    mail.send(msg)
    flash(f"Email sent to {request.form['email']} with your personal code", 'success')
    return code, user.email


@app.route('/reset', methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            global code
            global user_mail

            code, user_mail = get_code(user)
            return redirect(url_for('reset_code'))
        else:
            flash('Email not registered', 'danger')

    return render_template('reset.html', title='Reset Request')


@app.route('/password_reset', methods=['POST', 'GET'])
def reset_pass():
    user = User.query.filter_by(email=user_mail).first()
    if request.method == 'POST':
        hsh_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if bcrypt.check_password_hash(hsh_password, request.form['password']):
            user.password = hsh_password
            db.session.commit()
            flash('Password change successful, Log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match', 'success')
    return render_template('reset_pass.html', title='Password Reset')


@app.route('/reset_code', methods=['POST', 'GET'])
def reset_code():
    if request.method == 'POST':
        if code == request.form['reset']:
            return redirect(url_for('reset_pass'))
        else:
            flash('Wrong code', 'danger')

    return render_template('reset_code.html', title='Reset Code')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
