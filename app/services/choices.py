from flask import request, jsonify
from app.models import Choices
from config import db

## 선택지 생성
def create_choice(data):
    new_choice = Choices(
                    content = data['content'],
                    is_active = data['is_active'],
                    sqe = data['sqe'],
                    question_id = data['question_id']
                    )
    
    db.session.add(new_choice)
    db.session.commit()

    return new_choice

## 선택지 조회
def get_choice_by_id(question_id):
    choices = Choices.query.filter_by(question_id=question_id).all()
    return [choice.to_dict() for choice in choices] 


