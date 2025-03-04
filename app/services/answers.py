from flask import request, jsonify
from app.models import Answer
from config import db

# 답변 추가
def create_answer(data):
    new_answer = Answer(
                        user_id = data['user_id'],
                        choice_id = data['choice_id']
                        )
    
    db.session.add(new_answer)
    db.session.commit()

    return new_answer

# 답변 조회
def get_answers_by_id(answer_id):
    answers = Answer.query.all()
    return [answer.to_dict() for answer in answers]