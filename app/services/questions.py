from flask import request, jsonify
from app.models import Question, Choices, Image
from config import db

# 질문 생성
def create_question(data):
    title = data.get("title")
    is_active = data.get("is_active", True)
    sqe = data.get("sqe")
    image_id = data.get("image_id", None)

    # ✅ `image_id`가 없으면 기본값 설정
    if image_id is None:
        default_image = Image.query.first()  # ✅ images 테이블에서 첫 번째 이미지 가져오기
        image_id = default_image.id if default_image else 1  # ✅ 기본 이미지 ID (없으면 1)

    if not title or not sqe:
        return {"error": "title과 sqe는 필수입니다."}, 400


    new_question = Question(
        title=title,
        is_active=is_active,
        sqe=sqe,
        image_id=image_id
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
        "image_id": question.image_id,
        "image_url": question.image.url if question.image else None,
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
        "image_id": question.image_id,
        "image_url": question.image.url if question.image else None
    }


# 질문 수정
def update_question(question_id, data):
    question = Question.query.get_or_404(question_id)

    question.title = data.get("title", question.title)
    question.is_active = data.get("is_active", question.is_active)
    question.sqe = data.get("sqe", question.sqe)
    question.image_id = data.get("image_id", question.image_id)

    db.session.commit()

    return {"message": "Success updated question"}, 200


# 질문 삭제
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)

    db.session.delete(question)
    db.session.commit()

    return {"message": "Success deleted question"}, 200
