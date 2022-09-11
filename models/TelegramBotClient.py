import requests
import os
from urllib.parse import urlencode
from models.xmlsettings import XMLSettings


class TelegramBotClient(object):
    xml_file_name = 'conf_xml/telegram_conf.xml'
    update_id_tag = 'update_id'
    token_tag = 'token'
    group_id_tag = 'group_id'

    def __init__(self):
        self.config = XMLSettings(self.xml_file_name)
        self.api_token = self.config.get(self.token_tag, 'anu')
        self.group_id = self.config.get(self.group_id_tag, '-611864083')
        self.update_id = self.config.get(self.update_id_tag, '334231447')
        self.config.put(self.token_tag, self.api_token)
        self.config.put(self.group_id_tag, self.group_id)
        self.config.put(self.update_id_tag, self.update_id)
        self.config.save()

    def send_file(self, bytes_, caption):
        url = 'https://api.telegram.org/bot{}/sendPhoto?'.format(self.api_token)
        params = {'chat_id': self.group_id, 'caption': caption}

        with open(caption, 'wb') as f:
            f.write(bytes_)

        files = {'photo': None}
        resp = {'a': None}

        with open(caption, 'rb') as f:
            files['photo'] = f
            resp['a'] = requests.post(url + urlencode(params), files=files).json()

        if os.path.exists(caption):
            os.remove(caption)

        return resp['a']

    def reply_to(self, reply_to_message_id, text):
        url = 'https://api.telegram.org/bot{}/sendMessage?'.format(self.api_token)
        params = {'chat_id': self.group_id, 'text': text, 'reply_to_message_id': reply_to_message_id}

        return requests.post(url + urlencode(params)).json()

    def get_message_reply_to_text(self, message_id, update_id=None):
        if update_id is None:
            update_id = self.update_id
        elif update_id == self.update_id:
            return None, None

        url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'.format(self.api_token, update_id)
        resp = requests.post(url)
        results = resp.json()['result']

        for result in results:
            if result['message']['message_id'] > message_id and \
                    result['message']['reply_to_message']['message_id'] == message_id:
                self.update_id = result['update_id']
                self.config.put(self.update_id_tag, result['update_id'])
                self.config.save()

                return result['message']['text'], result['message']['message_id']

        self.update_id = results[0]['update_id']
        self.config.put(self.update_id_tag, results[0]['update_id'])
        self.config.save()

        return self.get_message_reply_to_text(message_id, update_id=results[0]['update_id'])

    def delete_message(self, message_id):
        url = 'https://api.telegram.org/bot{}/deleteMessage?'.format(self.api_token)
        params = {'chat_id': self.group_id, 'message_id': message_id}
        return requests.post(url + urlencode(params)).json()

    def send_message(self, text):
        url = 'https://api.telegram.org/bot{}/sendMessage?'.format(self.api_token)
        params = {'chat_id': self.group_id, 'text': text, 'parse_mode': 'html'}

        return requests.post(url + urlencode(params)).json()
