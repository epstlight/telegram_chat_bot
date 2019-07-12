import requests  #요청을 하기 위한 모듈 
from decouple import config  #.env안에 숨겨져 있는 변수를 가져올수 있는 모듈 그중에서 config함수를 이용하여 가져온다 .

base_url = 'https://api.telegram.org'
token = config('API_TOKEN')  #config('변수명') 보안성을 위하여 사용함. 

def sendM(chat_id, message):
    api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(api_url)
