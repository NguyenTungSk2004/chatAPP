from flask import Blueprint, request, jsonify, current_app
from app.models import Message, User
from app import db,allowed_file
from werkzeug.utils import secure_filename
import os
message_blueprint = Blueprint('messages', __name__)

# Gửi tin nhắn
@message_blueprint.route('/send', methods=['POST'])
def send_message():
    data = request.form
    
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    message_type = data.get('message_type')  # text, image, video
    
    # Kiểm tra dữ liệu hợp lệ
    if not sender_id or not receiver_id or not content:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra người gửi và người nhận có tồn tại
    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)
    if not sender or not receiver:
        return jsonify({"message": "User not found"}), 404
    

    media_path = None
    media_filename = None
    if 'media' in request.files:
        if media := request.files['media']:
            if not allowed_file(media.filename):
                return jsonify({"message": "Invalid file format"}), 400
            media_filename = secure_filename(media.filename)
            media_path = os.path.join(current_app.config['UPLOAD_FOLDER'], media_filename)
            media.save(media_path)

    # Tạo tin nhắn mới
    new_message = Message(
        sender_id=sender_id, 
        receiver_id=receiver_id, 
        content=content, 
        message_type=message_type, 
        media=media_path, 
        is_read=False
    )
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({"message": "Message sent successfully", "message_id": new_message.id}), 201

# Lấy tin nhắn giữa hai người
@message_blueprint.route('/conversation', methods=['GET'])
def get_conversation():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    # Kiểm tra dữ liệu hợp lệ
    if not sender_id or not receiver_id:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Lấy tin nhắn giữa hai người
    messages = Message.query.filter(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) | 
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    ).all()

    # Chuyển đổi danh sách tin nhắn thành JSON
    messages_list = [msg.to_dict() for msg in messages]
    
    return jsonify({"messages": messages_list}), 200
