# 베이스 이미지로 Python 3.10 사용
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . /app

# MariaDB 컨테이너가 준비될 때까지 대기 (10초 예시)
CMD ["sh", "-c", "sleep 10 && python main.py"]
