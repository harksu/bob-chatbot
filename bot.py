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
                results.append(f"입력된 IP: {ioc}를 기반으로 IoC를 조회하도록 하겠습니다. \n")
                vt_result = virustotal(ioc, 'ip') 
                results.append(f"VirusTotal 조회 결과\n")
                results.append(f"Harmless=> {vt_result['harmless']}건\n")      
                results.append(f"Malicious=> {vt_result['malicious']}건\n")    
                results.append(f"Suspicious=> {vt_result['suspicious']}건\n")   
                results.append(f"Timeout=> {vt_result['timeout']}건\n")
                results.append(f"Undetected=> {vt_result['undetected']}건\n")

                abuseipdb_result = abuseipdb_query(ioc)['data']
                results.append(f"AbuseIPDB 조회 결과\n")
                results.append(f"IsPublic=> {abuseipdb_result['isPublic']}\n")      
                results.append(f"IsWhitelisted=> {abuseipdb_result['isWhitelisted']}\n")    
                results.append(f"AbuseConfidenceScore=> {abuseipdb_result['abuseConfidenceScore']}점\n")   
                results.append(f"UsageType=> {abuseipdb_result['usageType']}\n")
                results.append(f"Domain=> {abuseipdb_result['domain']}\n")
                response_message = "\n".join(results)

                print(response_message)

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
