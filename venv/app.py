from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LogingForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:pepe1@localhost/users2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "test123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
app.app_context().push()


@app.route('/')
def home_page():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.username.data
        first_name = form.password.data
        last_name = form.username.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user'] = new_user.username
        flash(f'You made it! {new_user.username}')
        return redirect('/secret')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LogingForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"WelcomeBack, {user.username}!")
            session['user'] = user.username
            return redirect(f'/secret_to/users/{user.username}')
        else:
            form.username.errors = ['Invalid credentials.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user')
    flash(f"Goodbye!")
    return redirect('/')


@app.route('/secret')
def secret_reg():
    if 'user' not in session:
        flash("Sorry i can't Show you")
        return render_template('index.html')
         
   
    return render_template('/secret.html')


@app.route('/secret_to/users/<username>')
def secret(username):
    if 'user' not in session:
        
        flash("Sorry i can't Show you")
        return render_template('index.html')
         
   
    return render_template('/secret.html')


@app.route('/users/<username>',methods=['GET', 'POST'])
def users_feedback(username):
    user = User.query.get_or_404(username)
    if 'user' not in session:
        flash("Login please")
        return render_template('index.html')
    
    if session['user'] != username:
        flash("Not your Account")
        return render_template('index.html')
    
    feedbacks_list=user.feedbacks
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback.create(title, content, username)
        
        db.session.add(feedback)
        db.session.commit()
        flash("Thanks for your contribution")
        return redirect(f'/users/{username}')
    
    return render_template('users.html',user=user, form=form, feedbacks_list= feedbacks_list)



@app.route('/delete/<feedback_id>',methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    Feedback.query.filter(Feedback.id == feedback.id).delete()
    db.session.commit()

    return redirect(f'/users/{feedback.username}')




@app.route('/delete/user/<username>',methods=['POST'])
def delete_user(username):
    user = User.query.get_or_404(username)
    if 'user' not in session:
        flash("Login please")
        return render_template('index.html')
    if session['user'] != username:
        flash("Not your Account")
        return render_template('index.html')
    
    user = User.query.get(username)
    User.query.filter(User.username == user.username).delete()
    session.pop('user')
    db.session.commit()

    return redirect('/')


@app.route('/edit/<feedback_id>',methods=['GET','POST'])
def edit_feedback(feedback_id):
    feedback= Feedback.query.get(feedback_id)
    if 'user' not in session:
        flash("Login please")
        return render_template('index.html')
    if session['user'] != feedback.username:
        flash("Not your Feedback")
        return render_template('index.html')
    
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        Feedback.query.get(feedback_id).title=title
        Feedback.query.get(feedback_id).content=content
        db.session.commit()
        flash("Succes")
        return redirect(f'/users/{feedback.username}')
    
    return render_template('edit.html',form=form)