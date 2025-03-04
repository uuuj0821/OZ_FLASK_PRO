from flask import request, jsonify
from app.models import Question, Choices
from config import db

# 질문 생성
def create_question(data):
    new_question = Question(
                        title = data['title'],
                        is_active = data['is_active'],
                        sqe = data['sqe'],
                        image_id = data['image_id']
                        )
    
    db.session.add(new_question)
    db.session.commit()

    return new_question

# 질문 조회
def get_question_by_id(question_id):
    question = Question.query.get(question_id)    
    choices = [choice.to_dict() for choice in Choices.query.filter_by(question_id=question_id).all()]

    return {
        "id": question.id,
        "title": question.title,
        "image": question.image.url if question.image else None,
        "choices": choices
    }

# 질문 개수 조회
def count_question():
    return Question.query.count()