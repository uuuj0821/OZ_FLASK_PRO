from flask import request, jsonify
from app.models import Question, Choices
from config import db

# 질문 생성
def create_question(data):
    title = data.get("title")
    is_active = data.get("is_active", True)
    sqe = data.get("sqe")
    image = data.get("image")

    if not title or not sqe:
        return {"error": "title과 sqe는 필수입니다."}, 400

    new_question = Question(
        title=title,
        is_active=is_active,
        sqe=sqe,
        image=image
    )

    db.session.add(new_question)
    db.session.commit()

    return {"message": "Success", "question_id": new_question.id}, 201


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


# 특정 질문 조회
def get_one_question(question_id):
    question = Question.query.get_or_404(question_id)
    return {
        "id": question.id,
        "title": question.title,
        "is_active": question.is_active,
        "sqe": question.sqe,
        "image": question.image
    }


# 질문 수정
def update_question(question_id, data):
    question = Question.query.get_or_404(question_id)

    question.title = data.get("title", question.title)
    question.is_active = data.get("is_active", question.is_active)
    question.sqe = data.get("sqe", question.sqe)
    question.image = data.get("image", question.image)

    db.session.commit()

    return {"message": "Success updated question"}, 200


# 질문 삭제
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)

    db.session.delete(question)
    db.session.commit()

    return {"message": "Success deleted question"}, 200