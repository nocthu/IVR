from flask import Flask, render_template, session, redirect, request, url_for, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table

app = Flask(__name__)

# ENV = 'prod'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''
# # else:
app.debug = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pgyrprfvmjxjqm:ae7dcfa8630cadc1b8263d59077593207b55dbdb8fddbf0a9bc8d094893fc63f@ec2-52-206-44-27.compute-1.amazonaws.com:5432/d4q64kbe6gfnoo'
SQLALCHEMY_DATABASE_URI = 'postgres://pgyrprfvmjxjqm:ae7dcfa8630cadc1b8263d59077593207b55dbdb8fddbf0a9bc8d094893fc63f@ec2-52-206-44-27.compute-1.amazonaws.com:5432/d4q64kbe6gfnoo'

app.config['SQLALCHEMY_BINDS'] = {
    'users': SQLALCHEMY_DATABASE_URI,
    'posts': 'postgres://lsxgpxkbhcmidj:ede832ca91fa457fa7837b389bb07d9b03642708e47ef57de7d446f42ce35c4e@ec2-34-202-65-210.compute-1.amazonaws.com:5432/dc4v5190j2lbd0'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine(
    'postgres://pgyrprfvmjxjqm:ae7dcfa8630cadc1b8263d59077593207b55dbdb8fddbf0a9bc8d094893fc63f@ec2-52-206-44-27.compute-1.amazonaws.com:5432/d4q64kbe6gfnoo'
)
connection = engine.connect()
metadata = MetaData(engine)


# census = Table('posts', metadata, autoload=True)
census = Table('users', metadata, autoload=True)


class Posts(db.Model):  # бд постов
    __tablename__ = 'posts'
    __bind_key__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_aim = db.Column(db.String)
    post_type = db.Column(db.String)
    post_name = db.Column(db.String)
    post_required = db.Column(db.String)
    post_purpose = db.Column(db.String)
    post_author = db.Column(db.String)
    post_contacts = db.Column(db.String)
    post_date = db.Column(db.String)

    def __init__(self, post_aim, post_type, post_name, post_required, post_purpose, post_author, post_contacts, post_date):
        self.post_aim = post_aim
        self.post_type = post_type
        self.post_name = post_name
        self.post_required = post_required
        self.post_purpose = post_purpose
        self.post_author = post_author
        self.post_contacts = post_contacts
        self.post_date = post_date


class Users(db.Model):  # бд пользователей
    __tablename__ = 'users'
    __bind_key__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_nickname = db.Column(db.String, unique=True)
    user_email = db.Column(db.String, unique=True)
    user_name = db.Column(db.String)
    user_surname = db.Column(db.String)
    user_group = db.Column(db.String)
    user_password = db.Column(db.String)
    # user_posts = db.Column(db.String)

    def __init__(self, user_nickname, user_email, user_name, user_surname, user_group, user_password):
        self.user_nickname = user_nickname
        self.user_email = user_email
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_group = user_group
        self.user_password = user_password
        # self.user_posts = user_posts


app.config['SECRET_KEY'] = 'SECRET_KEY'


def main():
    app.run()


@app.before_request
def before_request():
    g.name = None
    g.surname = None
    g.usid = None

    if 'name' in session and 'surname' in session and 'usid' in session:
        g.name = session['name']
        g.surname = session['surname']
        g.usid = session['usid']


@app.route('/dropsession')
def dropsession():
    session.pop('name', None)
    session.pop('surname', None)
    session.pop('usid', None)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if g.name and g.surname and g.usid:
        return render_template('index.html', name=session['name'], surname=session['surname'], id=session['id'])

    if request.method == 'POST':
        session.pop('name', None)
        session.pop('surname', None)
        session.pop('usid', None)

        if request.form["btn"] == "Войти":
            nickname = request.form["nickname"]
            password = request.form["password"]

            user = db.session.query(Users).filter(Users.user_nickname == nickname,
                                                  Users.user_password == password).first()
            if user:
                name = user.user_name
                surname = user.user_surname
            else:
                message = "Неккоректные данные"

            session['name'] = name
            session['surname'] = surname
            session['usid'] = user.id

        elif request.form["btn"] == "Зарегистрироваться":
            nickname = request.form["nickname"]
            email = request.form["email"]
            name = request.form["name"]
            surname = request.form["surname"]
            group = request.form["group"]
            password = request.form["password"]

            oluser = db.session.query(Users).filter(
                Users.user_nickname == nickname).first()
            if oluser:
                message = "Никнейм уже занят"

            oluser = db.session.query(Users).filter(Users.user_email == email).first()
            if oluser:
                message = "Почта уже занята"

            user = Users(nickname, email, name, surname, group, password)
            db.session.add(user)
            db.session.commit()

            session['name'] = name
            session['surname'] = surname
            session['usid'] = user.id

        return render_template('index.html', surname=surname, name=name, id=user.id)

    return render_template('login.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        user_id = session['usid']
        prttype = request.form['prtype']
        prsub = request.form['prsub']
        probtype = request.form['probtype']
        name = request.form['name']
        demands = request.form['demands']
        description = request.form['description']
        href_vk = request.form['href_vk']
        href_telegram = request.form['href_telegram']
        href_google = request.form['href_google']

        return render_template('index.html')

    return render_template('add_post.html')


@app.route('/add_vacancy', methods=['GET', 'POST'])
def add_vacancy():
    if request.method == 'POST':
        user_id = session['usid']
        probtype = request.form['probtype']
        description = request.form['description']
        href_vk = request.form['href_vk']
        href_telegram = request.form['href_telegram']
        href_google = request.form['href_google']

        return render_template('index.html')

    return render_template('add_vacancy.html')


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        user_id = session['usid']
        name = request.form['name']
        description = request.form['description']
        href_quiz = request.form['href_quiz']
        href_vk = request.form['href_vk']
        href_telegram = request.form['href_telegram']
        href_google = request.form['href_google']
        
        return render_template('index.html')

    return render_template('add_quiz.html')


@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
    if request.method == 'POST':
        user_id = session['usid']
        prttype = request.form['prtype']
        prsub = request.form['prsub']
        probtype = request.form['probtype']
        name = request.form['name']
        description = request.form['description']

        return render_template('index.html')

    return render_template('add_idea.html')


if __name__ == '__main__':

    # posts = Posts()
    # posts.init_table()
    # users = Users()
    # users.init_table()

    main()
