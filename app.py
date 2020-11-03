from flask import Flask, render_template, session, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table

app = Flask(__name__)

# ENV = 'prod'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''
# # else:
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mcanmrnxroupdp:f260d4ac9d3d65eba6a7674825ad0b72e5d00c73f751a7bb7a7c8e86c8c7079d@ec2-52-1-95-247.compute-1.amazonaws.com:5432/d5srufilsb21f0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# engine = create_engine(
#     'postgres://mcanmrnxroupdp:f260d4ac9d3d65eba6a7674825ad0b72e5d00c73f751a7bb7a7c8e86c8c7079d@ec2-52-1-95-247.compute-1.amazonaws.com:5432/d5srufilsb21f0'
# )
# connection = engine.connect()
# metadata = MetaData(engine)


# # census = Table('posts', metadata, autoload=True)
# census = Table('users', metadata, autoload=True)


# class Posts(db.Model):  # бд постов
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     post_aim = db.Column(db.String)
#     post_type = db.Column(db.String)
#     post_name = db.Column(db.String)
#     post_required = db.Column(db.String)
#     post_purpose = db.Column(db.String)
#     post_author = db.Column(db.String)
#     post_contacts = db.Column(db.String)
#     post_date = db.Column(db.String)

#     def __init__(self, post_aim, post_type, post_name, post_required, post_purpose, post_author, post_contacts, post_date):
#         self.post_aim = post_aim
#         self.post_type = post_type
#         self.post_name = post_name
#         self.post_required = post_required
#         self.post_purpose = post_purpose
#         self.post_author = post_author
#         self.post_contacts = post_contacts
#         self.post_date = post_date

#
class Users(db.Model):  # бд пользователей
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    user_name = db.Column(db.String)
    user_surname = db.Column(db.String)
    user_group = db.Column(db.String)
    user_password = db.Column(db.String)
    # user_posts = db.Column(db.String)

    def __init__(self, user_email, user_name, user_password, user_group, user_posts):
        self.user_email = user_email
        self.user_name = user_name
        self.user_password = user_password
        self.user_group = user_group
        self.user_posts = user_posts


app.config['SECRET_KEY'] = 'SECRET_KEY'


def main():
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form["btn"] == "Войти":
            name = request.form["nickname"]
            password = request.form["password"]

        elif request.form["btn"] == "Зарегистрироваться":
            nickname = request.form["nickname"]
            email = request.form["email"]
            name = request.form["name"]
            surname = request.form["surname"]
            password = request.form["password"]

        return render_template('try.html')

    return render_template('login.html')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':

        return render_template('try.html')

    return render_template('add_post.html')


@app.route('/add_vacancy', methods=['GET', 'POST'])
def add_vacancy():
    if request.method == 'POST':

        return render_template('try.html')

    return render_template('add_vacancy.html')


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':

        return render_template('try.html')

    return render_template('add_quiz.html')


@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
    if request.method == 'POST':

        return render_template('try.html')

    return render_template('add_idea.html')


if __name__ == '__main__':

    # posts = Posts()
    # posts.init_table()
    # users = Users()
    # users.init_table()

    main()
