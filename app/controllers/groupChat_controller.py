from flask import Blueprint, request, jsonify
from app.models import GroupChat, GroupMember, User, GroupMessage
from app.extensions import db

group_chat_blueprint = Blueprint('group_chat', __name__)

# Tạo nhóm mới
@group_chat_blueprint.route('/create', methods=['POST'])
def create_group_chat():
    data = request.get_json()
    group_name = data.get('group_name')
    owner_id = data.get('owner_id')

    # Kiểm tra dữ liệu hợp lệ
    if not group_name or not owner_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra người tạo có tồn tại
    owner = User.query.get(owner_id)
    if not owner:
        return jsonify({"message": "Owner not found"}), 404

    # Tạo nhóm mới
    new_group = GroupChat(group_name=group_name, owner_id=owner_id)
    db.session.add(new_group)
    db.session.commit()

    # Tự động thêm người tạo làm thành viên nhóm
    owner_member = GroupMember(group_id=new_group.id, user_id=owner_id)
    db.session.add(owner_member)
    db.session.commit()

    return jsonify({"message": "Group created successfully", "group_id": new_group.id}), 201

#xóa nhóm
@group_chat_blueprint.route('/delete', methods=['POST'])
def delete_group_chat():
    data = request.get_json()
    group_id = data.get('id')

    # Kiểm tra dữ liệu hợp lệ
    if not group_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra nhóm chat có tồn tại
    group = GroupChat.query.get(group_id)
    if not group:
        return jsonify({"message": "Group not found"}), 404

    # Xóa nhóm chat
    db.session.delete(group)
    db.session.commit()

    return jsonify({"message": "Group deleted successfully"}), 200

# Cập nhật nhóm chat
@group_chat_blueprint.route('/update', methods=['PUT'])
def update_group_chat():
    data = request.form
    group_id = data.get('id')
    group_name = data.get('group_name')
    user_id = data.get('user_id')
    background = data.get('background')

    if not group_id or not user_id or not (group_name and background):
        return jsonify({"message": "Missing required fields"}), 400

    group =  GroupChat.query.get(group_id)
    if not group:
        return jsonify({"message": "Group not found"}), 404
    
    if not GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first():
        return jsonify({"message": "User not in group"}), 400
    
    if group_name:
        group.group_name = group_name
    if background:
        group.background = background
    db.session.commit()

    
