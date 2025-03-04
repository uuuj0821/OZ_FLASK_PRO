from flask import request, jsonify, abort
from app.models import User
from config import db

# 사용자 생성
def create_user(data):
    # 세션을 갱신하여 중복 검사 오류 방지
    db.session.expire_all()
    # 이메일 중복 검사
    if User.query.filter_by(email=data['email']).first():
        abort(400, "이미 존재하는 계정입니다.1")

    new_user = User(
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
                email = data['email']
                )
    
    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict()


# 특정 사용자 조회 (R)
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        abort(400, "사용자를 찾을 수 없습니다.")

    return user.to_dict()

# 사용자 전체 조회
def get_all_user():
    return [user.to_dict() for user in User.query.all()]

