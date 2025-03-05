from flask import request, jsonify
from app.models import Choices, Question
from config import db


# 특정 질문에 선택지 추가
def create_choice(question_id, text, is_correct):
    question = Question.query.get(question_id)
    if not question:
        return None  # 존재하지 않는 질문 ID

    new_choice = Choices(question_id=question_id, text=text, is_correct=is_correct)
    db.session.add(new_choice)
    db.session.commit()
    return new_choice.to_dict()


## 선택지 조회
def get_choice_by_id(question_id):
    choices = Choices.query.filter_by(question_id=question_id).all()
    return [choice.to_dict() for choice in choices] 


