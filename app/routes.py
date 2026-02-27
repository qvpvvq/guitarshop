from flask import render_template, request, redirect, url_for, flash
from .models import Guitar, User, db
from flask import current_app as app
from flask_login import login_user, logout_user

@app.route("/")
def index():
    items = Guitar.query.all()
    return render_template("cards.html", items=items)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Проверяем, нет ли уже такого юзера
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return "Такой юзер уже есть!"
            
        new_user = User(username=username)
        new_user.set_password(password) # Шифруем пароль
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index')) # После успеха кидаем на главную
        
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for("index"))
            else:
                return "Неверный пароль"
        else:
            return render_template("login.html", error="Такого пользователя не существует")
    if request.method == 'GET':
        return render_template("login.html")

            
@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for('index'))
