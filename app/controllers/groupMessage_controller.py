from flask import Blueprint, current_app , request, jsonify
from app.models import GroupChat, GroupMember, User, GroupMessage
from app import db, allowed_file
from werkzeug.utils import secure_filename
import os

group_message_blueprint = Blueprint('group_message', __name__)

# Lấy tin nhắn trong nhóm
@group_message_blueprint.route('/get_messages', methods=['GET'])
def get_group_messages():
    group_id = request.args.get('group_id')
    user_id = request.args.get('user_id')

    if not group_id or not user_id:
        return jsonify({"message": "Missing required fields"}), 400

    group = GroupChat.query.get(group_id)
    if not group:
        return jsonify({"message": "Group not found"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    memberOfThisGroup = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not memberOfThisGroup:
        return jsonify({"message": "User is not a member of this group"}), 403

    messages = GroupMessage.query.filter_by(group_id=group_id).all()
    messages = [message.to_dict() for message in messages]

    return jsonify(messages), 200

# Gửi tin nhắn trong nhóm
@group_message_blueprint.route('/send_message', methods=['POST'])
def send_group_message():
    # Các bước xử lý thông tin từ request
    group_id = request.form.get('group_id')
    sender_id = request.form.get('sender_id')
    content = request.form.get('content')
    message_type = request.form.get('message_type') #text/image/video

    if not group_id or not sender_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra nhóm chat, người gửi, và thành viên nhóm
    group = GroupChat.query.get(group_id)
    if not group:
        return jsonify({"message": "Group not found"}), 404

    sender = User.query.get(sender_id)
    if not sender:
        return jsonify({"message": "Sender not found"}), 404

    memberOfThisGroup = GroupMember.query.filter_by(group_id=group_id, user_id=sender_id).first()
    if not memberOfThisGroup:
        return jsonify({"message": "Sender is not a member of this group"}), 403

    media_filename = None
    media_path = None

    # Kiểm tra tệp đính kèm và lưu vào thư mục
    if 'media' in request.files:
        media_file = request.files['media']
        if media_file and allowed_file(media_file.filename):
            media_filename = secure_filename(media_file.filename)
            media_path = os.path.join(current_app.config['UPLOAD_FOLDER'], media_filename)
            media_file.save(media_path)
        else:
            return jsonify({"message": "Invalid file format"}), 400
    # Tạo và lưu tin nhắn
    new_message = GroupMessage(
        group_id=group_id,
        sender_id=sender_id,
        content=content,
        media=media_path,
        message_type=message_type,
        is_read=False
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully", "message_id": new_message.id}), 201
