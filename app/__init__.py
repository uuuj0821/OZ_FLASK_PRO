from flask import Flask, jsonify
from config import db
from flask_migrate import Migrate
from app.routes import main_blp
from app.routes import users_blp
from app.routes import questions_blp
from app.routes import images_blp 
from app.routes import choices_blp
from app.routes import answers_blp

import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    migrate.init_app(application, db)

    # 이어서 블루 프린트 등록 코드를 작성해주세요!

    application.register_blueprint(main_blp)
    application.register_blueprint(users_blp)
    application.register_blueprint(questions_blp)
    application.register_blueprint(images_blp)
    application.register_blueprint(choices_blp)
    application.register_blueprint(answers_blp)

    return application
