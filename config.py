import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

conf = {
    "log": os.getenv("LOG"),
    "dbpassword": os.getenv("DB_PASSWORD"),
    "virus_total_api_key": os.getenv("VIRUS_TOTAL_API_KEY"),
    "bot_token": os.getenv("BOB_TOKEN"),
    "socket_token": os.getenv("BOB_SOCKET")
}
