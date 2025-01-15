from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db, allowed_file
from werkzeug.utils import secure_filename
import os
import bcrypt # type: ignore

auth_blueprint = Blueprint('auth', __name__)

# Đăng ký người dùng
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Kiểm tra dữ liệu hợp lệ
    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra nếu người dùng đã tồn tại
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400
    
    # Mã hóa mật khẩu bằng bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Tạo người dùng mới
    new_user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# Đăng nhập người dùng
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
        
    email = data.get('email')
    password = data.get('password')
    
    # Kiểm tra dữ liệu hợp lệ
    if not email or not password:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Kiểm tra người dùng có tồn tại
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "Invalid credentials"}), 401
    
    user.status = "online"
    response = {
        "message": "Login successful", 
        "user":{
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }
    return jsonify(response), 200

# Lấy thông tin người dùng
@auth_blueprint.route('/get_user', methods=['GET'])
def get_user():
    data = request.form

    id = data.get('id')

    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# Cập nhật thông tin người dùng
@auth_blueprint.route('/update', methods=['PUT'])
def update_user():
    data = request.form

    id = data.get('id')
    email = data.get('email')
    phone = data.get('phone')
    avatar = data.get('avatar')

    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not avatar and 'avatar' in request.files:
        if avatar_file := request.files['avatar']:
            if not allowed_file(avatar_file.filename):
                return jsonify({"message": "Invalid file format"}), 400
            avatar_filename = secure_filename(avatar_file.filename)
            avatar = os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename)
            avatar_file.save(avatar)
    
    user.avatar = avatar
    user.email = email
    user.phone = phone

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200
# Quên mật khẩu
@auth_blueprint.route('/forgetPassword', methods=['POST'])
def forget_password():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')

    user = User.query.filter_by(email=email, username=username).first()
    if not user:
        return jsonify({"message": "Account not found"}), 404
    # Send notification to email provider
    '''
        my code send notification to email provider
        ...
    '''
    return jsonify({"message": "Email found"}), 200

# Đổi lại mật khẩu
@auth_blueprint.route('/changePassword', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    retype_password = data.get('retype_password')

    if password != retype_password:
        return jsonify({"message": "Password not match"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Account not found"}), 404
    
    user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.session.commit()
