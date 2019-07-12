from flask import Flask, request, render_template
from decouple import config
import pprint, requests

app = Flask(__name__)

API_TOKEN = config('API_TOKEN')  #상수는 대문자
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')

@app.route('/')
def hello():
    return 'hello world'


def sendM(chat_id, message):
    base_url = 'https://api.telegram.org'
    api_url = f'{base_url}/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(api_url)


@app.route(f'/{API_TOKEN}', methods=['POST']) #이 route로는 Post로만 정보를 받겠다.
def telegram():
    from_telegram = request.get_json()  #요청 받아오기, dict Type

    if from_telegram.get('message') is not None:
        #우리가 원하는 로직 
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

        if text[0:4] == '/한영 ':  #번역 tool
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,  #trailing comma
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:],
            }  
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data).json()
            # pprint.pprint(papago_res)
            text = papago_res.get('message').get('result').get('translatedText')
        
        if text[0:4] == '/영한 ':  #번역 tool
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,  #trailing comma
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:],
            }  
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data).json()
            # pprint.pprint(papago_res)
            text = papago_res.get('message').get('result').get('translatedText')
        
        sendM(chat_id, text)        


    return ''


if __name__ == "__main__":
    app.run(debug=True)
