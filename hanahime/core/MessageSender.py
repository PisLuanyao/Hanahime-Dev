import requests


class MessageSender:
    @staticmethod
    def send_message(method, url):
        response = requests.request(method, url)
        if response.status_code == 200:
            print('Message sent successfully')
        else:
            print('Failed to send message')

    @staticmethod
    def post_message(method, url, json_data=None):
        headers = {'Content-Type': 'application/json'}
        response = requests.request(method, url, headers=headers, json=json_data)
        if response.status_code == 200:
            print('Message sent successfully')
        else:
            print('Failed to send message')
