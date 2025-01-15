from flask import Flask
from app.extensions import db
from app.controllers import *
import os

app = Flask(__name__)

# Cấu hình thư mục lưu trữ tệp
app.config['UPLOAD_FOLDER'] =  os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Cấu hình kết nối đến SQL Server (SQL Server Express)
app.config['SQLALCHEMY_DATABASE_URI'] = r'mssql+pyodbc://TUNGSK\SQLEXPRESS/ChatAPP?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo các phần mở rộng
db.init_app(app)

# Đăng ký các blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(message_blueprint, url_prefix='/messages')
app.register_blueprint(group_chat_blueprint, url_prefix='/group_chat')
app.register_blueprint(group_message_blueprint, url_prefix='/group_message')
app.register_blueprint(group_member_blueprint, url_prefix='/group_member')

if __name__ == "__main__":
    app.run(debug=True)
