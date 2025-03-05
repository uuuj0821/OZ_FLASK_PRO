from app.models import User
from config import db


# 모든 유저 조회
def get_all_users():
    users = User.query.all()
    return [user.to_dict() for user in users]


# 특정 유저 조회
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "존재하지 않는 유저 ID입니다."}, 404
    return user.to_dict(), 200


# 새로운 유저 생성
def create_user(username, email):
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return {"error": "이미 존재하는 유저명 또는 이메일입니다."}, 400

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict(), 201
