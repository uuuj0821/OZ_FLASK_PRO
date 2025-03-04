from flask import Flask, jsonify
from flask_migrate import Migrate
import app.models
from app.routes import route_bp
from config import db
from flask_smorest import Api

migrate = Migrate()

def create_app():
    application = Flask(__name__)

    # swagger-ui
    application.config['API_TITLE'] = 'OZ Form API'
    application.config['API_VERSION'] = '1.0'
    application.config['OPENAPI_VERSION'] = '3.1.3'
    application.config['OPENAPI_URL_PREFIX'] = '/' 
    application.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui' 
    application.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(application)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)
    migrate.init_app(application, db)

	# 400 에러 발생 시, JSON 형태로 응답 반환
    @application.errorhandler(400)
    def handle_bad_request(error):
        response = jsonify({"message": error.description})
        response.status_code = 400
        return response

	# 블루프린트 등록
    api.register_blueprint(route_bp)

    return application