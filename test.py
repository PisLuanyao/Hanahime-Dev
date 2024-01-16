import requests


def post_message(method, url, json_data=None):
    headers = {'Content-Type': 'application/json'}
    response = requests.request(method, url, headers=headers, json=json_data)
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print('Failed to send message')


data = {"message": "pong"}  # POST请求的数据
post_message('POST', 'http://127.0.0.1:5000', json_data=data)
