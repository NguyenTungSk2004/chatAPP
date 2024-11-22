from app.extensions import db

class GroupChat(db.Model):
    __tablename__ = 'group_chats'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    creator = db.relationship('User', foreign_keys=[created_by])

    def __repr__(self):
        return f"<GroupChat {self.group_name}>"
