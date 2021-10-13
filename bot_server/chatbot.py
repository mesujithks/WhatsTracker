from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from db import DBHelper
import json
import requests
import time
import urllib
import threading
import logging

TOKEN = "<your telegram bot token enter here>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
ADMIN_CAHT_ID = "<your telegram user chat id for the bot>"


app = Flask(__name__)
CORS(app)
exit_event = threading.Event()

#logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger("WhatsTracker-logger")
log.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler = logging.FileHandler("app.log")
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def echo_all(updates, dataBase):
    log.info(updates)
    for update in updates["result"]:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        print(chat_id)
        send_message(text, chat_id) 

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    get_url(url)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    dataBase = DBHelper()
    dataBase.setup()
    last_update_id = None
    while exit_event.is_set():
        print(last_update_id)
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates, dataBase)
        time.sleep(0.5)

@app.route('/API/notifyAdmin', methods=['POST'])
def sendExpMessage():
    body = request.get_json()
    logging.info(body)
    print(body)
    dataBaseExp = DBHelper()
    dataBaseExp.add_user(body['user_name'], body['online_status'], body['active_time'])
    if(body['online_status'] == 'true'):
        send_message("User {} is online".format(body['user_name']), ADMIN_CAHT_ID)
    else:
        send_message("User {} is offline".format(body['user_name']), ADMIN_CAHT_ID)
    return jsonify(
        status="OK",
        message="Notified admin"
    )

if __name__ == '__main__':
    exit_event.set()
    chatbot = threading.Thread(target=main, args=())
    chatbot.daemon = True
    chatbot.start()
    try:
        app.run()
    except KeyboardInterrupt:
        exit_event.clear()
        chatbot.join()
    