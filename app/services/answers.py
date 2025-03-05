from flask import request, jsonify
from app.models import Answer, User, Question, Choices
from config import db


# 사용자의 답변 저장
def create_answer(choice_id, user_id):
    choice = Choices.query.get(choice_id)

    new_answer = Answer( choice_id=choice_id, user_id=user_id)
    db.session.add(new_answer)
    db.session.commit()
    return new_answer.to_dict(), 201


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