from flask import Blueprint, request, jsonify, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from app.models import User

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def create():
    """회원가입"""
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    gender = data.get("gender")
    age = data.get("age")
    password = data.get("password")

    if not all([name, email, gender, age, password]):
        return jsonify({"message": "모든 필드를 입력해야 합니다."}), 400

    # 중복 이메일 확인
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "이미 존재하는 계정입니다."}), 400

    # 성별 및 나이
    allowed_ages = {"teen", "twenty", "thirty", "fourty", "fifty"}
    allowed_genders = {"male", "female"}

    if age not in allowed_ages:
        return jsonify({"message": f"Invalid age: {age}. Allowed values: {allowed_ages}"}), 400

    if gender not in allowed_genders:
        return jsonify({"message": f"Invalid gender: {gender}. Allowed values: {allowed_genders}"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, gender=gender, age=age, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "회원가입 성공!"}), 201


@bp.route("/login", methods=["POST"])
def login():
    """로그인 및 세션 설정"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "이메일 또는 비밀번호가 잘못되었습니다."}), 401

    session['user_id'] = user.id
    return jsonify({"message": "로그인 성공!"})


@bp.route("/profile", methods=["GET"])
def get_profile():
    """사용자 프로필 조회"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "로그인이 필요합니다."}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404

    return jsonify(user.to_dict())


@bp.route("/update", methods=["PUT"])
def update_user():
    """사용자 정보 수정"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "로그인이 필요합니다."}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.gender = data.get("gender", user.gender)
    user.age = data.get("age", user.age)

    if "password" in data and data["password"]:
        user.password = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify({"message": "사용자 정보가 수정되었습니다."})


@bp.route("/logout", methods=["POST"])
def logout():
    """로그아웃"""
    session.pop('user_id', None)
    return jsonify({"message": "로그아웃 되었습니다."})


@bp.route("/delete", methods=["DELETE"])
def delete_user():
    """사용자 계정 삭제"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "로그인이 필요합니다."}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404

    db.session.delete(user)
    db.session.commit()

    session.pop('user_id', None)
    return jsonify({"message": "계정이 삭제되었습니다."})
