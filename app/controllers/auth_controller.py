import bcrypt
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db

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
    
    return jsonify({"message": "Login successful", "user": {"username": user.username, "email": user.email}}), 200
