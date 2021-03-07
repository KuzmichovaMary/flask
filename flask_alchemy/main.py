from flask import Flask, render_template, redirect
from flask_alchemy.data import db_session
from flask_alchemy.data.jobs import Jobs
from flask_alchemy.data.users import User
from flask_alchemy.forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success")
def success():
    return redirect('/')


@app.route("/")
def main_page():
    d = []
    db_sess = db_session.create_session()
    for job in db_sess.query(Jobs):
        j = {}
        leader = db_sess.query(User).filter(User.id == job.team_leader).first()
        leader = f"{leader.name} {leader.surname}"
        id = str(job.id)
        duration = f"{job.work_size} hours"
        collaborators = job.collaborators
        finished = job.is_finished
        job = job.job
        j["id"] = id
        j["duration"] = duration
        j["leader"] = leader
        j["list"] = collaborators
        j["finished"] = finished
        j["job"] = job
        d.append(j)
    return render_template("log.html", jobs=d)


def add_user(surname, name, age, position, speciality, address, email, db_sess):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    db_sess.add(user)
    db_sess.commit()


def main():
    db_session.global_init("flask_alchemy/db/mars_explorer.db")
    app.run(port=8081)


if __name__ == '__main__':
    main()
