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

load_dotenv()

BOT_TOKEN = os.getenv("BOB_TOKEN")
SOCKET_TOKEN = os.getenv("BOB_SOCKET")

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
            logging.info(message_text.startswith("ioc "))
            if message_text.startswith("ioc "):
                ioc = message_text.split(" ")[1]
                results = []
                border_line = ":heavy_minus_sign:" * 20
                

                results.append(f":mag: 입력된 IP: {ioc}를 기반으로 IoC를 조회하도록 하겠습니다.")
                results.append(f"{border_line}")

                vt_result = virustotal(ioc, 'ip') 
                results.append(f":white_check_mark: VirusTotal 조회 결과")
                results.append(f":skull_and_crossbones: Harmless => {vt_result['harmless']}건")      
                results.append(f":biohazard_sign: Malicious => {vt_result['malicious']}건")    
                results.append(f":warning: Suspicious => {vt_result['suspicious']}건")   
                results.append(f":hourglass_flowing_sand: Timeout => {vt_result['timeout']}건")
                results.append(f":grey_question: Undetected => {vt_result['undetected']}건")

                
                results.append(f"{border_line}")

                results.append(f":shield: AbuseIPDB 조회 결과")
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
                print("useage: type ioc <ip_address>")

if __name__ == "__main__":
    try:
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        SLACK_CLIENT.connect()
        Event().wait()
    except Exception as main_e:
        error = str(main_e)
        logging.warning('main func: %s', error)
