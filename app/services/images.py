from app.models import Image
from config import db

def get_all_images():
    # 모든 이미지 데이터를 조회
    images = Image.query.all()
    return [image.to_dict() for image in images]

def create_image(url, description):
    # 새로운 이미지 데이터를 생성
    new_image = Image(url=url, description=description)
    db.session.add(new_image)
    db.session.commit()
    return new_image.to_dict()
