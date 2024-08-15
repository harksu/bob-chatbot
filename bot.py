from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from dotenv import load_dotenv
from vt import virustotal
from abuseipdb import abuseipdb_query 
import logging
import os
from threading import Event
import requests


load_dotenv()

BOT_TOKEN = os.getenv("BOB_TOKEN")
SOCKET_TOKEN = os.getenv("BOB_SOCKET")
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "http://localhost:8080")  


SLACK_CLIENT = SocketModeClient(
    app_token=SOCKET_TOKEN,
    web_client=WebClient(token=BOT_TOKEN)
)

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        if req.payload["event"]["type"] == "message" \
            and req.payload["event"].get("subtype") is None:
            
            message_text = req.payload["event"]["text"]
            channel_id = req.payload["event"]["channel"]
            if message_text.startswith("bob-wiki:"):
                name = message_text.split("bob-wiki:")[1].strip()
                if name:
                    results = []
                    response = requests.get(f"{FASTAPI_HOST}/developtechs/{name}")
                    if response.status_code == 200:
                        data = response.json()
                        results.append(f"🏷️이름: {data['name']}\n")
                        results.append(f"🌟특징: {data['description']}\n")  
                        results.append(f"🔁습관: {data['habit']}\n") 
                        results.append(f"🍶소주: {data['soju_count']}병\n")  
                        response_message = "\n".join(results)
                    else:
                        response_message = "해당 이름으로 데이터를 찾을 수 없습니다."
                    client.web_client.chat_postMessage(channel=channel_id, text=response_message)
                else:
                    client.web_client.chat_postMessage(channel=channel_id, text="이름을 입력해 주세요.")

            elif message_text.startswith("ioc "):
                ioc = message_text.split(" ")[1]
                results = []
                border_line = ":heavy_minus_sign:" * 20
                

                results.append(f":mag: 입력된 IP: {ioc}를 기반으로 IoC를 조회하도록 하겠습니다.")
                
                vt_result = virustotal(ioc, 'ip') 
                
                results.append(f"{border_line}")
                results.append(f":white_check_mark: VirusTotal 조회 결과")
                results.append(f"{border_line}")

                results.append(f":skull_and_crossbones: Harmless => {vt_result['harmless']}건")      
                results.append(f":biohazard_sign: Malicious => {vt_result['malicious']}건")    
                results.append(f":warning: Suspicious => {vt_result['suspicious']}건")   
                results.append(f":hourglass_flowing_sand: Timeout => {vt_result['timeout']}건")
                results.append(f":grey_question: Undetected => {vt_result['undetected']}건")

                
                results.append(f"{border_line}")
                results.append(f":shield: AbuseIPDB 조회 결과")
                results.append(f"{border_line}")
                
                abuseipdb_result = abuseipdb_query(ioc)['data']
                results.append(f":globe_with_meridians: IsPublic => {abuseipdb_result['isPublic']}")
                results.append(f":no_entry_sign: IsWhitelisted => {abuseipdb_result['isWhitelisted']}")    
                results.append(f":triangular_flag_on_post: AbuseConfidenceScore => {abuseipdb_result['abuseConfidenceScore']}점")   
                results.append(f":computer: UsageType => {abuseipdb_result['usageType']}")
                results.append(f":house: Domain => {abuseipdb_result['domain']}")

                results.append(f"{border_line}")
            
                response_message = "\n".join(results)

                client.web_client.chat_postMessage(channel=channel_id, text=response_message)
            else:
                print("useage: 이거 나중에 사용법 적자")

if __name__ == "__main__":
    try:
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        SLACK_CLIENT.connect()
        Event().wait()
    except Exception as main_e:
        error = str(main_e)
        logging.warning('main func: %s', error)
