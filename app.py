import os
from flask import Flask, redirect, url_for
from config import Config
from db import init_db
from auth import auth_bp
from child_routes import child_bp
from parent_routes import parent_bp
from pet_routes import pet_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 首次运行初始化数据库
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db()

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(parent_bp)
    app.register_blueprint(child_bp)
    app.register_blueprint(pet_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)