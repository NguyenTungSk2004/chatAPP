from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask import current_app 

# Tạo đối tượng db
db = SQLAlchemy()

# Kiểm tra định dạng tệp hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']