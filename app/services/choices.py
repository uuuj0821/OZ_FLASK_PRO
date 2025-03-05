from flask import request, jsonify
from app.models import Choices, Question
from config import db


# 특정 질문에 선택지 추가
def create_choice(data):
    content = data.get("content")
    is_active = data.get("is_active", True)
    sqe = data.get("sqe")
    question_id = data.get("question_id")

    print(content, is_active, sqe, question_id)

    new_choice = Choices(content=content, is_active=is_active, sqe=sqe, question_id=question_id)
    db.session.add(new_choice)
    db.session.commit()
    return new_choice.to_dict()


## 선택지 조회
def get_choice_by_id(question_id):
    choices = Choices.query.filter_by(question_id=question_id).all()
    return [choice.to_dict() for choice in choices] 


