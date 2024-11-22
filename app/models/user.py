from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    avatar = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<User {self.username}>"
