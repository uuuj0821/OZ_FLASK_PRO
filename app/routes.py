from flask import Blueprint, request, jsonify
from app.services.questions import (
    get_all_questions, get_one_question,
    create_question, update_question, delete_question
)
from app.services.users import get_all_users, get_user_by_id, create_user
from app.services.images import get_all_images, create_image
from app.services.choices import get_choices_by_question, create_choice
from app.services.answers import get_answers_by_question, create_answer

main_blp = Blueprint("main", __name__)

users_blp = Blueprint("users", __name__, url_prefix="/users")
questions_blp = Blueprint("questions", __name__, url_prefix="/questions")
images_blp = Blueprint("images", __name__, url_prefix="/images")
choices_blp = Blueprint("choices", __name__, url_prefix="/choices")
answers_blp = Blueprint("answers", __name__, url_prefix="/answers")


# 기본 연결 확인 API
@main_blp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Success Connect"}), 200


# 전체 유저 조회 API
@users_blp.route("/users", methods=["GET"])
def fetch_users():
    users = get_all_users()
    return jsonify(users), 200


# 특정 유저 조회 API
@users_blp.route("/<int:user_id>", methods=["GET"])
def fetch_user(user_id):
    user, status_code = get_user_by_id(user_id)
    return jsonify(user), status_code


# 새로운 유저 생성 API
@users_blp.route("/", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "username, email 필드는 필수입니다."}), 400

    user, status_code = create_user(username=data["username"], email=data["email"])
    return jsonify(user), status_code



# 전체 질문 조회 & 생성
@questions_blp.route("/", methods=["GET", "POST"])
def handle_questions():
    if request.method == "GET":
        return jsonify(get_all_questions()), 200
    elif request.method == "POST":
        data = request.json
        return jsonify(create_question(data))


# 특정 질문 조회, 수정, 삭제
@questions_blp.route("/<int:question_id>", methods=["GET", "PUT", "DELETE"])
def handle_question(question_id):
    if request.method == "GET":
        return jsonify(get_one_question(question_id)), 200
    elif request.method == "PUT":
        data = request.json
        return jsonify(update_question(question_id, data))
    elif request.method == "DELETE":
        return jsonify(delete_question(question_id))
    

# 전체 이미지 조회 API
@images_blp.route("/", methods=["GET"])
def fetch_images():
    images = get_all_images()
    return jsonify(images), 200


# 새 이미지 추가 API
@images_blp.route("/", methods=["POST"])
def add_image():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL 필드는 필수입니다."}), 400

    image = create_image(url=data["url"], description=data.get("description"))
    return jsonify(image), 201



# 특정 질문의 선택지 조회 API
@choices_blp.route("/<int:question_id>", methods=["GET"])
def fetch_choices(question_id):
    choices = get_choices_by_question(question_id)
    return jsonify(choices), 200


# 새 선택지 추가 API
@choices_blp.route("/", methods=["POST"])
def add_choice():
    data = request.get_json()
    if not data or "question_id" not in data or "text" not in data:
        return jsonify({"error": "question_id 및 text 필드는 필수입니다."}), 400

    choice = create_choice(question_id=data["question_id"], text=data["text"], is_correct=data.get("is_correct", False))
    
    if choice is None:
        return jsonify({"error": "존재하지 않는 질문 ID입니다."}), 400

    return jsonify(choice), 201



# 특정 질문의 답변 조회 API
@answers_blp.route("/<int:question_id>", methods=["GET"])
def fetch_answers(question_id):
    answers = get_answers_by_question(question_id)
    return jsonify(answers), 200



# 사용자 답변 추가 API
@answers_blp.route("/", methods=["POST"])
def add_answer():
    data = request.get_json()
    if not data or "question_id" not in data or "choice_id" not in data or "user_id" not in data:
        return jsonify({"error": "question_id, choice_id, user_id 필드는 필수입니다."}), 400

    answer, status_code = create_answer(
        question_id=data["question_id"],
        choice_id=data["choice_id"],
        user_id=data["user_id"]
    )

    return jsonify(answer), status_code