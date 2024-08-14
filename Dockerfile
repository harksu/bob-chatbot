# 베이스 이미지로 Python 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치를 위해 패키지 관리자를 업데이트
RUN apt-get update && apt-get install -y gcc

# requirements.txt 파일을 복사하고 의존성 설치
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 포트 설정
EXPOSE 8080

# main.py 실행 명령어
CMD ["python", "main.py"]
