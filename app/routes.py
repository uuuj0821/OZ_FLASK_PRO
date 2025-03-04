from flask import request, jsonify
from flask_smorest import Blueprint
from app.services.users import create_user, get_user_by_id, get_all_user
from app.services.questions import create_question, get_question_by_id, count_question
from app.services.choices import create_choice, get_choice_by_id
from app.services.answers import create_answer, get_answers_by_id
from app.services.images import create_image, get_image_by_id

route_bp = Blueprint('main', __name__, description='OZ_FLASK_PRO API')

## 1. 기본 연결 확인 (/ get)
@route_bp.route('/', methods=['GET'])
def check_connect():
    if request.method == 'GET':
        return jsonify({"message":"Success Connect"}), 200


## 2. 메인 이미지 가져오기 (/image/main get)
@route_bp.route('/image/main', methods=['GET'])
def get_main_image():
    if request.method == 'GET':
        image = get_image_by_id()
        return jsonify({"image":image.url}), 200


## 3. 회원가입(/signup post)
@route_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET': # 전체 사용자 조회 // 나중에 삭제
        try:
            return jsonify(get_all_user()), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        try:
            user = create_user(data)

            return jsonify({"message":f"{user['name']}님 회원가입을 축하합니다",
                            "user_id":user['id']}), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 4. 질문 가져오기
## 4-1. 특정질문가져오기 (/questions/<int:question_id>  get)
@route_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    if request.method == 'GET':
        try:
            question = get_question_by_id(question_id)
            return jsonify(question), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 4-2. 질문 개수 확인 (/questions/count  get)
@route_bp.route('/questions/count', methods=['GET'])
def check_count_question():
    if request.method == 'GET':
        try:
            count = count_question()
            return jsonify({"totla":count}), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 5. 선택지 가져오기 (/choice/<int:questions_id> get)
@route_bp.route('/choice/<int:question_id>', methods=['GET'])
def get_choice(question_id):
    if request.method == 'GET':
        try:
            choice = get_choice(question_id)
            return jsonify(choice), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 6. 답변제출하기 (/submit post) 
@route_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        try:
            create_answer(data)
            user_id = data[0]["user_id"]
            return jsonify({"message":f"User: {user_id}'s answers Success Create"})
        except Exception as e:
            return jsonify({"message":str(e)})


## 7-1. 이미지생성 (/image post)
@route_bp.route('/image', methods=['GET', 'POST'])
def post_image():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        try:
            image = create_image(data)    
            return jsonify({"message":f"ID: {image.id} Image Success Create"})
        except Exception as e:
            return jsonify({"message":str(e)})


## 7-2. 질문생성 (/question  post)
@route_bp.route('/question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        try:
            question = create_question(data)
            return jsonify({"message":"Title: 새로운 질문 question Success Create"})
        except Exception as e:
            return jsonify({"message":str(e)})


## 7-3. 선택지 생성 (/choice post)
@route_bp.route('/choice', methods=['GET', 'POST'])
def post_choice():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        try:
            choice = create_choice(data)
            return jsonify({"message":"Content: 새로운 선택지 choice Success Create"})
        except Exception as e:
            return jsonify({"message":str(e)})