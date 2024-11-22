from flask import Blueprint, request, jsonify
from app.models import Message, User
from app.extensions import db

message_blueprint = Blueprint('messages', __name__)

# Gửi tin nhắn
@message_blueprint.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    message_type = data.get('message_type')  # text, image, video
    media = data.get('media')  # Đường dẫn tới tệp media (nếu có)
    
    # Kiểm tra dữ liệu hợp lệ
    if not sender_id or not receiver_id or not content:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra người gửi và người nhận có tồn tại
    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)
    if not sender or not receiver:
        return jsonify({"message": "User not found"}), 404
    
    # Tạo tin nhắn mới
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, 
                          message_type=message_type, media=media, is_read=False)
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
    messages_list = [{"sender_id": msg.sender_id, "receiver_id": msg.receiver_id, 
                      "content": msg.content, "message_type": msg.message_type, 
                      "sent_at": msg.sent_at, "is_read": msg.is_read} for msg in messages]
    
    return jsonify({"messages": messages_list}), 200
