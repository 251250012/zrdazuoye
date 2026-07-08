import os
from flask import Flask, redirect, url_for
from config import Config
from db import init_db, get_db
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
    else:
        # 数据库迁移
        with app.app_context():
            db = get_db()
            try:
                db.execute("ALTER TABLE pet ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                db.commit()
            except Exception:
                pass
            try:
                db.execute("ALTER TABLE user ADD COLUMN parent_id INTEGER DEFAULT NULL")
                db.commit()
            except Exception:
                pass

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
    app.run(host='0.0.0.0', port=8080)