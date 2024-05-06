import requests


class MessageSender:
    def send_message(self, method, url):
        response = requests.request(method, url)
        if response.status_code == 200:
            print('Message sent successfully')
        else:
            print('Failed to send message')

    def post_message(self, method, url, json_data=None):
        headers = {'Content-Type': 'application/json'}
        response = requests.request(method, url, headers=headers, json=json_data)
        if response.status_code == 200:
            print('Message sent successfully')
        else:
            print('Failed to send message')
