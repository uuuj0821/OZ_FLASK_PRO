from config import db
from app.models import Answer, User, Choices


def create_answer(user_id, choice_id):
    """답변 생성"""
    user = User.query.get(user_id)  # 주어진 user_id에 해당하는 사용자를 데이터베이스에서 조회
    if not user:
        raise ValueError("유효하지 않은 사용자 ID입니다.")  # 사용자가 존재하지 않으면 오류 발생

    choice = Choices.query.get(choice_id)  # 주어진 choice_id에 해당하는 선택지를 데이터베이스에서 조회
    if not choice:
        raise ValueError("유효하지 않은 선택지 ID입니다.")  # 선택지가 존재하지 않으면 오류 발생

    new_answer = Answer(user_id=user_id, choice_id=choice_id)  # 새로운 Answer 객체 생성
    db.session.add(new_answer)  # 데이터베이스에 추가
    db.session.commit()  # 변경사항 저장
    return new_answer  # 생성된 답변 객체 반환


def get_all_answers():
    """모든 답변 조회"""
    return Answer.query.all()  # Answer 테이블의 모든 데이터 조회 후 반환


def get_answer_by_id(answer_id):
    """특정 답변 조회"""
    return Answer.query.get(answer_id)  # 주어진 answer_id에 해당하는 답변을 조회 후 반환


def delete_answer(answer):
    """답변 삭제"""
    db.session.delete(answer)  # 주어진 Answer 객체를 데이터베이스에서 삭제
    db.session.commit()  # 변경사항 저장
