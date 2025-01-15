from app.extensions import db

class GroupMessage(db.Model):
    __tablename__ = 'group_messages'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_chats.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    media = db.Column(db.Text)
    message_type = db.Column(db.String(20))
    sent_at = db.Column(db.DateTime, default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    group = db.relationship('GroupChat', foreign_keys=[group_id])

    def __repr__(self):
        return f"<GroupMessage {self.id} in group {self.group.group_name} by {self.sender.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "media": self.media,
            "message_type": self.message_type,
            "sent_at": self.sent_at,
            "is_read": self.is_read
        }