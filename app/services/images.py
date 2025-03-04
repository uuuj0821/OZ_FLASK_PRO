from flask import request, jsonify
from app.models import Image
from config import db

## 이미지 생성
def create_image(data):
    new_image = Image(
                    url = data['url'],
                    type = data['type']
                    )
    
    db.session.add(new_image)
    db.session.commit()

    return new_image

## 이미지 조회
def get_image_by_id(image_id):
    image = Image.query.filter_by(type="main").first()
    return {"image": image.url}