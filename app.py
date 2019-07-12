from flask import Flask, request, render_template
from decouple import config
import pprint, requests

app = Flask(__name__)
API_TOKEN = config('API_TOKEN')  #상수는 대문자

@app.route('/')
def hello():
    return 'hello world'

def sendM(chat_id, message):
    api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(api_url)

@app.route(f'/{API_TOKEN}', methods=['POST']) #이 route로는 Post로만 정보를 받겠다.
def telegram():
    from_telegram = request.get_json()  #요청 받아오기, dict Type

    if from_telegram.get('message') is not None:
        #우리가 원하는 로직 
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

        if text == '!점심메뉴':
            text = '먹든가'
            sendM(chat_id, text)

    return ''


if __name__ == "__main__":
    app.run(debug=True)
