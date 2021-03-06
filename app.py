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
    'posts': 'postgres://ibuxjgsxkmjzjj:47c35c8abfdf583d06ef30ced185a5a9f96a78b32f616569f8c5a410ea6f770a@ec2-3-224-38-18.compute-1.amazonaws.com:5432/d3ch1omoaa82f6'
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
    user_name = db.Column(db.String)
    user_surname = db.Column(db.String)
    post_type = db.Column(db.Integer) # для себя - 1, вакансия - 2, опрос - 3, идея - 4
    project_type = db.Column(db.String) # тип ИВР
    subject = db.Column(db.String) # предмет ИВР
    problem_type = db.Column(db.String) # сфера поставленной задачи
    name = db.Column(db.String)
    demands = db.Column(db.String)
    description = db.Column(db.String)
    href_vk = db.Column(db.String)
    href_telegram = db.Column(db.String)
    href_google = db.Column(db.String)
    href_quiz = db.Column(db.String)
    date = db.Column(db.String)

    def __init__(self, user_id, user_name, user_surname, 
                    post_type, project_type, subject, problem_type, name, demands, description, 
                    href_vk, href_telegram, href_google, href_quiz, date):
        self.user_id = user_id
        self.user_name = user_name
        self.user_surname = user_surname
        # self.href_vk = href_vk
        # self.href_telegram = href_telegram
        # self.href_google = href_google
        self.post_type = post_type
        self.project_type = project_type
        self.subject = subject
        self.problem_type = problem_type
        self.name = name
        self.demands = demands
        self.description = description
        self.href_vk = href_vk
        self.href_telegram = href_telegram
        self.href_google = href_google
        self.href_quiz = href_quiz
        self.date = date



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
# xR"V\c5%*c^raLV{j@5BD??".\&Fe+

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
        all_posts = db.session.query(Posts).all()
        post = []
        vacancy = []
        quiz = []
        idea = []
        for i in all_posts:
            if i.post_type == 1:
                if i.user_id != g.usid:
                    post.append([
                        i.user_name, i.user_surname, i.project_type, 
                        i.subject, i.problem_type, i.name, i.demands, i.description, 
                        i.href_vk, i.href_telegram, i.href_google
                    ])
            elif i.post_type == 2:
                if i.user_id != g.usid:
                    vacancy.append([
                        i.user_name, i.user_surname, 
                        i.problem_type, i.description, 
                        i.href_vk, i.href_telegram, i.href_google
                    ])
            elif i.post_type == 3:
                if i.user_id != g.usid:
                    quiz.append([
                        i.user_name, i.user_surname, 
                        i.name, i.description, 
                        i.href_vk, i.href_telegram, i.href_google, i.href_quiz
                    ])
            elif i.post_type == 4:
                if i.user_id != g.usid:
                    idea.append([
                        i.project_type, i.subject, i.name, i.description
                    ])

            post.reverse()
            vacancy.reverse()
            quiz.reverse()
            idea.reverse()
            
        return render_template('index.html', name=session['name'], surname=session['surname'], 
                                post=post, vacancy=vacancy, quiz=quiz, idea=idea)

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
                return redirect(url_for('index'))

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
                return redirect(url_for('index'))

            oluser = db.session.query(Users).filter(Users.user_email == email).first()
            if oluser:
                message = "Почта уже занята"
                return redirect(url_for('index'))

            user = Users(nickname, email, name, surname, group, password)
            db.session.add(user)
            db.session.commit()

            session['name'] = name
            session['surname'] = surname
            session['usid'] = user.id

        all_posts = db.session.query(Posts).all()
        post = []
        vacancy = []
        quiz = []
        idea = []
        for i in all_posts:
            if i.post_type == 1:
                if i.user_id != user.id:
                    post.append([
                        i.user_name, i.user_surname, i.project_type, 
                        i.subject, i.problem_type, i.name, i.demands, i.description, 
                        i.href_vk, i.href_telegram, i.href_google
                    ])
            elif i.post_type == 2:
                if i.user_id != user.id:
                    vacancy.append([
                        i.user_name, i.user_surname, 
                        i.problem_type, i.description, 
                        i.href_vk, i.href_telegram, i.href_google
                    ])
            elif i.post_type == 3:
                if i.user_id != user.id:
                    quiz.append([
                        i.user_name, i.user_surname, 
                        i.name, i.description, 
                        i.href_vk, i.href_telegram, i.href_google, i.href_quiz
                    ])
            elif i.post_type == 4:
                if i.user_id != user.id:
                    idea.append([
                        i.user_name, i.user_surname, i.project_type, 
                        i.subject, i.problem_type, i.name, i.description, 
                        i.href_vk, i.href_telegram, i.href_google
                    ])

            post.reverse()
            vacancy.reverse()
            quiz.reverse()
            idea.reverse()
            

        return render_template('index.html', surname=surname, name=name, 
                                post=post, vacancy=vacancy, quiz=quiz, idea=idea)

    return render_template('login.html')


@app.route('/myposts', methods=['GET'])
def myposts():
    # if request.method == 'POST':



    #     return redirect(url_for('index'))

    all_posts = db.session.query(Posts).filter(
                Posts.user_id == g.usid
            ).all()
    post = []
    vacancy = []
    quiz = []
    idea = []
    for i in all_posts:
        if i.post_type == 1:
            post.append([
                i.user_name, i.user_surname, i.project_type, 
                i.subject, i.problem_type, i.name, i.demands, i.description, 
                i.href_vk, i.href_telegram, i.href_google, i.id
            ])
        elif i.post_type == 2:
            vacancy.append([
                i.user_name, i.user_surname, 
                i.problem_type, i.description, 
                i.href_vk, i.href_telegram, i.href_google, i.id
            ])
        elif i.post_type == 3:
            quiz.append([
                i.user_name, i.user_surname, 
                i.name, i.description, 
                i.href_vk, i.href_telegram, i.href_google, i.href_quiz, i.id
            ])
        elif i.post_type == 4:
            idea.append([
                i.user_name, i.user_surname, i.project_type, 
                i.subject, i.problem_type, i.name, i.description, 
                i.href_vk, i.href_telegram, i.href_google, i.id
            ])

    return render_template('myposts.html', post=post, vacancy=vacancy, quiz=quiz, idea=idea)


@app.route('/delete/<int:id>')
def delete(id):
    post_delete = db.session.query(Posts).filter(Posts.id==id).first()

    db.session.delete(post_delete)
    db.session.commit()

    return redirect(url_for('myposts'))


@app.route('/update/post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    post_update = db.session.query(Posts).filter(Posts.id==id).first()
    if request.method == 'POST':
        # post_update = request.form['name']

        post_update.project_type = request.form.get('type')
        post_update.subject = request.form.get('subject')
        post_update.problem_type = request.form.get('problemtype')
        post_update.name = request.form["name"]
        post_update.demands = request.form["demands"]
        post_update.description = request.form["description"]
        post_update.href_vk = request.form["href_vk"]
        post_update.href_telegram = request.form["href_telegram"]
        post_update.href_google = request.form["href_google"]
        db.session.commit()

        return redirect(url_for('myposts'))
    return render_template('update_post.html', post_update=post_update)


@app.route('/update/vacancy/<int:id>', methods=['GET', 'POST'])
def update_vacancy(id):
    post_update = db.session.query(Posts).filter(Posts.id==id).first()
    if request.method == 'POST':
        # post_update = request.form['name']

        post_update.problem_type = request.form.get('problemtype')
        post_update.description = request.form['description']
        post_update.href_vk = request.form['href_vk']
        post_update.href_telegram = request.form['href_telegram']
        post_update.href_google = request.form['href_google']
        db.session.commit()

        return redirect(url_for('myposts'))
    return render_template('update_vacancy.html', post_update=post_update)


@app.route('/update/quiz/<int:id>', methods=['GET', 'POST'])
def update_quiz(id):
    post_update = db.session.query(Posts).filter(Posts.id==id).first()
    if request.method == 'POST':
        # post_update = request.form['name']

        post_update.name = request.form['name']
        post_update.description = request.form['description']
        post_update.href_quiz = request.form['href_quiz']
        post_update.href_vk = request.form['href_vk']
        post_update.href_telegram = request.form['href_telegram']
        post_update.href_google = request.form['href_google']
        db.session.commit()

        return redirect(url_for('myposts'))
    return render_template('update_quiz.html', post_update=post_update)


@app.route('/update/idea/<int:id>', methods=['GET', 'POST'])
def update_idea(id):
    post_update = db.session.query(Posts).filter(Posts.id==id).first()
    if request.method == 'POST':
        # post_update = request.form['name']

        post_update.project_type = request.form.get('type')
        post_update.subject = request.form.get('subject')
        post_update.problem_type = request.form.get('problemtype')
        post_update.name = request.form['name']
        post_update.description = request.form['description']

        db.session.commit()

        return redirect(url_for('myposts'))
    return render_template('update_idea.html', post_update=post_update)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        user_id = session['usid']
        user_name = session['name']
        user_surname = session['surname']
        post_type = 1
        project_type = request.form.get('type')
        subject = request.form.get('subject')
        problem_type = request.form.get('problemtype')
        name = request.form["name"]
        demands = request.form["demands"]
        description = request.form["description"]
        href_vk = request.form["href_vk"]
        href_telegram = request.form["href_telegram"]
        href_google = request.form["href_google"]
        href_quiz = None
        date = None

        post = Posts(user_id, user_name, user_surname, post_type, 
                    project_type, subject, problem_type, name, demands, description, 
                    href_vk, href_telegram, href_google, href_quiz, date)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_post.html')


@app.route('/add_vacancy', methods=['GET', 'POST'])
def add_vacancy():
    if request.method == 'POST':
        user_id = session['usid']
        user_name = session['name']
        user_surname = session['surname']
        post_type = 2
        problem_type = request.form.get('problemtype')
        description = request.form['description']
        href_vk = request.form['href_vk']
        href_telegram = request.form['href_telegram']
        href_google = request.form['href_google']

        project_type = None
        subject = None
        name = None
        demands = None
        href_quiz = None
        date = None

        post = Posts(user_id, user_name, user_surname, post_type, 
                    project_type, subject, problem_type, name, demands, description, 
                    href_vk, href_telegram, href_google, href_quiz, date)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_vacancy.html')


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        user_id = session['usid']
        user_name = session['name']
        user_surname = session['surname']
        post_type = 3
        name = request.form['name']
        description = request.form['description']
        href_quiz = request.form['href_quiz']
        href_vk = request.form['href_vk']
        href_telegram = request.form['href_telegram']
        href_google = request.form['href_google']

        project_type = None
        subject = None
        problem_type = None
        demands = None
        date = None

        post = Posts(user_id, user_name, user_surname, post_type, 
                    project_type, subject, problem_type, name, demands, description, 
                    href_vk, href_telegram, href_google, href_quiz, date)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('add_quiz.html')


@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
    if request.method == 'POST':
        user_id = session['usid']
        user_name = session['name']
        user_surname = session['surname']
        post_type = 4
        project_type = request.form.get('type')
        subject = request.form.get('subject')
        problem_type = request.form.get('problemtype')
        name = request.form['name']
        description = request.form['description']

        demands = None
        href_vk = None
        href_telegram = None
        href_google = None
        href_quiz = None
        date = None

        post = Posts(user_id, user_name, user_surname, post_type, 
                    project_type, subject, problem_type, name, demands, description, 
                    href_vk, href_telegram, href_google, href_quiz, date)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_idea.html')


if __name__ == '__main__':

    main()
