from flask import request, jsonify
from app.models import Answer, User, Question, Choices
from config import db


# 사용자의 답변 저장
def create_answer(choice_id, user_id):
    # 선택지(Choice) 존재 여부 확인
    choice = Choices.query.get(choice_id)
    if not choice:
        return {"error": "유효하지 않은 choice_id입니다."}, 400

    # 사용자(User) 존재 여부 확인 (선택적)
    user = User.query.get(user_id)
    if not user:
        return {"error": "유효하지 않은 user_id입니다."}, 400

    # 새로운 답변 객체 생성
    new_answer = Answer(choice_id=choice_id, user_id=user_id)

    db.session.add(new_answer)
    db.session.commit()

    return new_answer.to_dict()  # Flask가 자동으로 200 OK 처리


# 답변 조회
def get_answers_by_id(answer_id):
    answers = Answer.query.all()
    return [answer.to_dict() for answer in answers]


# 특정 질문에 대한 모든 답변 조회
def get_answers_by_question(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    return [answer.to_dict() for answer in answers]


def delete_answer(answer):
    """답변 삭제"""
    db.session.delete(answer)  # 주어진 Answer 객체를 데이터베이스에서 삭제
    db.session.commit()  # 변경사항 저장
