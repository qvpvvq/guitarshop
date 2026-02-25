from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Guitar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    form = db.Column(db.String(50))
    model = db.Column(db.String(50))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))