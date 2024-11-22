from app.extensions import db

class GroupMember(db.Model):
    __tablename__ = 'group_members'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=db.func.now())

    group = db.relationship('GroupChat', backref=db.backref('members', lazy=True))
    user = db.relationship('User', backref=db.backref('groups', lazy=True))

    def __repr__(self):
        return f"<GroupMember user {self.user.username} in group {self.group.group_name}>"
