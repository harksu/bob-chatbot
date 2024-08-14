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
                print(ioc)

                vt_result = virustotal(ioc, 'ip')  # 예시로 IP 타입 사용
                print(vt_result)
                #logging.CRITICAL(f"VirusTotal: {vt_result}")
               # results.append(f"VirusTotal: {vt_result}")

                abuseipdb_result = abuseipdb_query(ioc)
                #logging.CRITICAL(f"AbuseIPDB: {abuseipdb_result}")
               # results.append(f"AbuseIPDB: {abuseipdb_result}")
                print(abuseipdb_result)
              #  response_message = "\n".join(results)
              #  print(response_message)
              #  client.web_client.chat_postMessage(channel=channel_id, text=response_message)
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
