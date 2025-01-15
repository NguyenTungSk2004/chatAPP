from flask import Blueprint, request, jsonify
from app.models import GroupChat, GroupMember, User
from app.extensions import db

group_member_blueprint= Blueprint('group_member', __name__)

# Thêm thành viên vào nhóm
@group_member_blueprint.route('/add_member', methods=['POST'])
def add_member():
    data = request.get_json()
    group_id = data.get('group_id')
    user_id = data.get('user_id')

    # Kiểm tra dữ liệu hợp lệ
    if not group_id or not user_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra nhóm và người dùng có tồn tại
    group = GroupChat.query.get(group_id)
    user = User.query.get(user_id)
    if not group:
        return jsonify({"message": "Group not found"}), 404
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Kiểm tra người dùng đã là thành viên chưa
    existing_member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    if existing_member:
        return jsonify({"message": "User is already a member of the group"}), 400

    # Thêm thành viên mới
    new_member = GroupMember(group_id=group_id, user_id=user_id)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member added successfully"}), 201

# Xóa thành viên khỏi nhóm
@group_member_blueprint.route('/remove_member', methods=['DELETE'])
def remove_member():
    data = request.get_json()
    group_id = data.get('group_id')
    user_id = data.get('user_id')

    # Kiểm tra dữ liệu hợp lệ
    if not group_id or not user_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra thành viên có tồn tại trong nhóm
    member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not member:
        return jsonify({"message": "Member not found in the group"}), 404

    # Xóa thành viên
    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": "Member removed successfully"}), 200

# Lấy danh sách thành viên trong nhóm
@group_member_blueprint.route('/members', methods=['GET'])
def get_members():
    group_id = request.args.get('group_id')

    # Kiểm tra dữ liệu hợp lệ
    if not group_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Lấy danh sách thành viên
    members = GroupMember.query.filter_by(group_id=group_id).all()
    if not members:
        return jsonify({"message": "Group has no members"}), 404

    members_list = [
        {
            "user_id": member.user_id, 
            "user_name": User.query.get(member.user_id).username
        } for member in members
    ]

    return jsonify({"members": members_list}), 200
