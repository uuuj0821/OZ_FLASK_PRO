from flask import request, jsonify, abort
from app.models import Image
from config import db

## 이미지 생성
def create_image(url, image_type):
    # 새로운 이미지 데이터를 생성
    new_image = Image(url=url, image_type=image_type)

    db.session.add(new_image)
    db.session.commit()

    return new_image.to_dict()

## 이미지 조회
def get_image_by_id(image_id):
    image = Image.query.get(image_id) # id를 기준으로 검색

    if not image:
        abort(404, "Image not found")

    return {"image": image.url}

## 메인 이미지 조회
def get_main_image():
    image = Image.query.filter_by(image_type="main").first()

    if not image:
        abort(404, "Image not found")

    return {"image": image.url}


def get_all_images():
    # 모든 이미지 데이터를 조회
    images = Image.query.all()
    return [image.to_dict() for image in images]

