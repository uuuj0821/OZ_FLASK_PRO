from app.models import Answer, Question, Choices
from config import db


# 특정 질문에 대한 모든 답변 조회
def get_answers_by_question(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    return [answer.to_dict() for answer in answers]


# 사용자의 답변 저장
def create_answer(question_id, choice_id, user_id):
    question = Question.query.get(question_id)
    choice = Choices.query.get(choice_id)

    if not question:
        return {"error": "존재하지 않는 질문 ID입니다."}, 400

    if not choice or choice.question_id != question_id:
        return {"error": "유효하지 않은 선택지 ID입니다."}, 400

    new_answer = Answer(question_id=question_id, choice_id=choice_id, user_id=user_id)
    db.session.add(new_answer)
    db.session.commit()
    return new_answer.to_dict(), 201
