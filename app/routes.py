from flask import request, jsonify
from flask_smorest import Blueprint
from app.services.users import create_user, get_user_by_id, get_all_users
from app.services.questions import create_question, get_question_by_id, count_question
from app.services.choices import create_choice, get_choice_by_id
from app.services.answers import create_answer, get_answers_by_id, get_answers_by_question, delete_answer
from app.services.images import create_image, get_image_by_id,get_main_image

# 블루프린트 설정
main_blp = Blueprint("main", __name__)
questions_blp = Blueprint("questions", __name__, url_prefix="/questions")
image_blp = Blueprint("image", __name__, url_prefix="/image")
choice_blp = Blueprint("choice", __name__, url_prefix="/choice")
answers_blp = Blueprint("answers", __name__, url_prefix="/answers")
users_blp = Blueprint("users", __name__, url_prefix="/users")


## 1. 기본 연결 확인 (/ get)
@main_blp.route('/', methods=['GET'])
def check_connect():
    if request.method == 'GET':
        return jsonify({"message":"Success Connect"}), 200


## 2. 메인 이미지 가져오기 (/image/main get)
@image_blp.route('/main', methods=['GET'])
def view_main_image():
    if request.method == 'GET':
        image = get_main_image()
        return jsonify(image), 200


## 3. 회원가입(/signup post)
@main_blp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET': # 전체 사용자 조회 // 나중에 삭제
        try:
            return jsonify(get_all_users()), 200
        except Exception as e:
            return jsonify({"message":str(e)}), 400
        
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"message":"Invalid JSON data"}), 400
        
        try:
            user = create_user(data)

            return jsonify({"message":f"{user['name']}님 회원가입을 축하합니다",
                            "user_id":user['id']}), 200
        except Exception as e:
            print(f"Signup error: {e}")
            return jsonify({"message":str(e)}), 400


## 4. 질문 가져오기
## 4-1. 특정질문가져오기 (/questions/<int:question_id>  get)
@questions_blp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    if request.method == 'GET':
        try:
            question = get_question_by_id(question_id)
            return jsonify(question), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 4-2. 질문 개수 확인 (/questions/count  get)
@questions_blp.route('/count', methods=['GET'])
def check_count_question():
    if request.method == 'GET':
        try:
            count = count_question()
            return jsonify({"totla":count}), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 5. 선택지 가져오기 (/choice/<int:questions_id> get)
@choice_blp.route('/<int:question_id>', methods=['GET'])
def view_choice(question_id):
    if request.method == 'GET':
        try:
            choice = get_choice_by_id(question_id)
            return jsonify(choice), 200
        except Exception as e:
            return jsonify({"message":str(e)})


## 6. 답변제출하기 (/submit post) 
@main_blp.route('/submit', methods=['GET', 'POST'])
def submit_answer():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "데이터는 리스트 형식이어야 합니다."}), 400
        
        try:
            for entry in data:
                question_id = entry.get("question_id")
                choice_id = entry.get("choice_id")
                user_id = entry.get("user_id")
                
                if not all([question_id, choice_id, user_id]):
                    return jsonify({"error": "모든 필드를 입력해야 합니다 (question_id, choice_id, user_id)."}), 400
                
                create_answer(question_id, choice_id, user_id)
            
            user_id = data[0]["user_id"]
            return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 201
        except Exception as e:
            return jsonify({"message":str(e)})


## 7-1. 이미지생성 (/image post)
@image_blp.route('/', methods=['GET', 'POST'])
def post_image():
    if request.method == 'GET':
        try:
            return jsonify({"message":"Success"}), 200
        except Exception as e:
            return jsonify({"message":str(e)})
        
    if request.method == 'POST':
        data = request.get_json()

        # data가 None이거나 "url"과 "type"이 없을 경우 예외 처리
        if not data or "url" not in data or "type" not in data:
            return jsonify({"error": "이미지 URL과 type이 필요합니다."}), 400
        
        url = data["url"]
        image_type = data["type"]

        # print(data)
        # print(url)
        # print(image_type)
        # return jsonify({"message":"Success"}), 200

        try:
            image = create_image(url, image_type)
            return jsonify({"message":f"ID: {image['id']} Image Success Create"})
        except Exception as e:
            return jsonify({"message":str(e)})


## 7-2. 질문생성 (/question  post)
@main_blp.route('/question', methods=['GET', 'POST'])
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
@choice_blp.route('/', methods=['GET', 'POST'])
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
        

## 답변
@answers_blp.route("/", methods=["GET", "POST"])
def answers_get():
    if request.method == 'GET':
        return jsonify([a.to_dict() for a in get_answers_by_question()])  # 모든 답변을 JSON 형태로 반환
    
    if request.method == 'POST':
        data = request.get_json()  # 요청에서 JSON 데이터를 가져옴
    try:
        answer = create_answer(data["user_id"], data["choice_id"])  # 답변 생성 함수 호출
        return jsonify({"message": "답변이 생성되었습니다.", "answer": answer.to_dict()}), 201  # 성공 응답 반환
    except ValueError as e:
        return jsonify({"message": str(e)}), 400  # 유효하지 않은 입력값일 경우 오류 메시지 반환


@answers_blp.route("/<int:answer_id>", methods=["DELETE"])
def answer_delete(answer_id):
    """특정 답변 삭제 API"""
    answer = get_answers_by_id(answer_id)  # 주어진 ID에 해당하는 답변 조회
    if not answer:
        return jsonify({"message": "답변을 찾을 수 없습니다."}), 404  # 답변이 없을 경우 오류 메시지 반환
    delete_answer(answer)  # 답변 삭제 함수 호출
    return jsonify({"message": "답변이 삭제되었습니다."})  # 성공 응답 반환


# 전체 유저 조회 API
@users_blp.route("/", methods=["GET"])
def fetch_users():
    users = get_all_users()
    return jsonify(users), 200