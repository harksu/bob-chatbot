import virustotal3.core
import json
import os
from dotenv import load_dotenv  
from config import conf

load_dotenv()

api_key = os.getenv("VIRUS_TOTAL_API_KEY")

def virustotal(query_item, query_type):
    print(f'virustotal({query_type}): {query_item}')
    """ virustotal api """
    result = {}
    if query_type == 'ip':
        virus_total = virustotal3.core.IP(api_key)
        result = virus_total.info_ip(query_item)
       
    elif query_type == 'domain':
        virus_total = virustotal3.core.Domains(api_key)  
        result = virus_total.info_domain(query_item)
    elif query_type == 'url':
        virus_total = virustotal3.core.URL(api_key)
        result = virus_total.info_url(query_item)
    elif query_type == 'hash':
        virus_total = virustotal3.core.Files(api_key)
        result = virus_total.info_file(query_item)
   
    # 결과가 문자열로 반환될 수 있으므로 JSON으로 파싱 시도
    if isinstance(result, str):
        result = json.loads(result)
    
    if isinstance(result, dict):
        if 'data' in result and 'attributes' in result['data']: 
            return result['data']['attributes']['last_analysis_stats']
        else: 
            return {"error": "Invalid data structure", "result": result}
    else:
        return {"error": "Response is not a valid JSON object", "result": result}
  

