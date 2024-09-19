from main_app.extensions import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique = True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Student {self.username}>'