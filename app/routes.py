from flask import Flask, request, jsonify, session
from config import db
from app.services.users import create_user, authenticate_user, get_user_by_id, update_user, delete_user
from app.services.questions import get_all_questions, get_question_by_id, create_question, update_question, delete_question
from app.services.answers import get_all_answers, get_answer_by_id, create_answer, delete_answer

def create_app():
    """Flask 애플리케이션 생성 및 설정"""
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)

    """choices 코드"""

    """images 코드"""

    """questions 코드"""

    """users 코드"""

    """answers 코드"""
    @app.route("/answers", methods=["GET"])
    def answers_get():
        """모든 답변 조회 API"""
        return jsonify([a.to_dict() for a in get_all_answers()])  # 모든 답변을 JSON 형태로 반환

    @app.route("/answers", methods=["POST"])
    def answer_create():
        """답변 생성 API"""
        data = request.get_json()  # 요청에서 JSON 데이터를 가져옴
        try:
            answer = create_answer(data["user_id"], data["choice_id"])  # 답변 생성 함수 호출
            return jsonify({"message": "답변이 생성되었습니다.", "answer": answer.to_dict()}), 201  # 성공 응답 반환
        except ValueError as e:
            return jsonify({"message": str(e)}), 400  # 유효하지 않은 입력값일 경우 오류 메시지 반환

    @app.route("/answers/<int:answer_id>", methods=["DELETE"])
    def answer_delete(answer_id):
        """특정 답변 삭제 API"""
        answer = get_answer_by_id(answer_id)  # 주어진 ID에 해당하는 답변 조회
        if not answer:
            return jsonify({"message": "답변을 찾을 수 없습니다."}), 404  # 답변이 없을 경우 오류 메시지 반환
        delete_answer(answer)  # 답변 삭제 함수 호출
        return jsonify({"message": "답변이 삭제되었습니다."})  # 성공 응답 반환

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)