from app import create_app  # Flask 앱을 생성하는 함수가 있는 모듈을 가져옴

app = create_app()  # Flask 애플리케이션 인스턴스 생성

if __name__ == "__main__":
    app.run()
