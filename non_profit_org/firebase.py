import requests
import json

SERVER_KEY = "AAAAEeZ4Yos:APA91bHkiBQcWS0E3cbq-12EdqmMV_Xz-QCoKpw0bpm1iSs1QpFwG3KGcTPiBfXAoTHsFh3cV6PxgQ5RyK6IKXTUXpvffFoNY0VGizoL0yQK0hZu_H9boQFDilmg_LXFi0p46_a4e96X"
URL = "https://fcm.googleapis.com/fcm/send"


def _send_push(user, text):
    to = user.firebase_token.strip()
    if to == '':
        return
    _send_notification({
        'to': to,
        'notification': {
            'sound': 'default',
            'title': 'Приложение NPO',
            'body': text
        },
    })


def _send_notification(data):
    # if settings.DEBUG:
    #     return
    headers = {'Content-Type': 'application/json',
               'Authorization': 'key={0}'.format(SERVER_KEY)}
    request_data = json.dumps(data)
    requests.post(URL, headers=headers, data=request_data)
