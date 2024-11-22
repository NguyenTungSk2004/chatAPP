from flask import Flask
from app.extensions import db
from app.controllers import auth_blueprint, message_blueprint

app = Flask(__name__)

# Cấu hình kết nối đến SQL Server (SQL Server Express)
app.config['SQLALCHEMY_DATABASE_URI'] = r'mssql+pyodbc://TUNGSK\SQLEXPRESS/ChatAPP?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo các phần mở rộng
db.init_app(app)

# Đăng ký các blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(message_blueprint, url_prefix='/messages')

if __name__ == "__main__":
    app.run(debug=True)
