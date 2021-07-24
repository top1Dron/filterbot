import requests

API_link = 'https://api.telegram.org/bot1939365709:AAGoGjG48o0WognBg8Yxj5rRc3_oiX87Vas'

updates = requests.get(f'{API_link}/getUpdates?offset=-1').json()
# updates = requests.get(f'{API_link}/sendMessage?chat_id=588974925&text=Hello,%20my%20fellow%20brother!')

# print(updates)

message = updates['result'][0]['message']

chat_id = message['from']['id']
text = message['text']

send_message = requests.get(f'{API_link}/sendMessage?chat_id={chat_id}&text=Ты написал это сообщение: {text}')