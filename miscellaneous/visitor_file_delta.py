import datetime
import hashlib
import hmac
import json
import os
import time
import uuid

import requests


class WebimSdkSimulatorError(RuntimeError):

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.message}'


class WebimSdkSimulator:

    BASE_URL = 'https://dev.webimdev.ru'

    class Endpoint:
        DELTA = '/l/v/m/delta'
        ACTION = '/l/v/m/action'
        FILE_UPLOAD = '/l/v/m/upload'

    def __init__(self):
        # Node: increase DELTA_LIVE_PERIOD to 3000 to catch deltas before their removal
        self.device_id = WebimSdkSimulator.generate_random_device_id()
        self.push_token = WebimSdkSimulator.generate_random_push_token()
        self.page_id = None
        self.auth_token = None
        self.file_data = None
        self.private_key = '804952af584599cb027bf83d65ae8bcc'  # account-config: private_key

    def run(self):
        try:
            self.__run()
        except WebimSdkSimulatorError as e:
            print(e)

    def __run(self):
        response_data = self.make_init_request()
        self.page_id = response_data['fullUpdate']['pageId']
        self.auth_token = response_data['fullUpdate']['authToken']

        _ = self.make_chat_start_request()
        #
        # response_data = self.make_file_upload_request()
        # self.file_data = response_data
        #
        # _ = self.make_chat_file_message_request()

        # time.sleep(10)

        _ = self.make_chat_message_request()

        _ = self.make_delta_list_request()

    @staticmethod
    def generate_random_device_id():
        return f'device-id/{datetime.datetime.now().ctime()}'

    @staticmethod
    def generate_random_push_token():
        return f'token/{datetime.datetime.now().ctime()}'

    @staticmethod
    def make_request(url, method, params, files=None):
        if method == 'get':
            response = requests.get(url=url, params=params)
        elif method == 'post':
            response = requests.post(url=url, params=params, files=files)
        else:
            raise WebimSdkSimulatorError(message=f'unsupported method {method}')

        response.raise_for_status()

        response_data = response.json()
        if response_data.get('error'):
            raise WebimSdkSimulatorError(message=response_data['error'])

        print('#' * 80)
        print(json.dumps(response_data, indent=4, sort_keys=True))
        print('#' * 80)

        return response_data

    def make_init_request(self):
        """
        Initializes client.
        """
        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.DELTA}',
            method='get',
            params={
                'device-id': self.device_id,  # device-id is being created on event=init only
                'event': 'init',
                'respond-immediately': 1,  # used in `if since != self.get_current_revision() or waiter.request_handler.get_argument('respond-immediately', 'false') == 'true'`
                'push-token': self.push_token,
                'platform': 'ios',
                'since': 0,  # todo: needed?
                'title': 'My chat',
                'visitor': {
                    'creationTs': 1598971324.5726359,
                    'id': '7eae9563e990efd09145ed3b5bf3de2b',
                    'icon': {
                        'color': '#eeef65',
                        'shape': 'star'
                    },
                    'hasProvidedFields': False,
                    'modificationTs': 1616677207.2526541,
                    'stored': True
                },
                'visitor-ext': self.prepare_visitor_ext()
            }
        )

    def make_chat_start_request(self):
        """
        Request to start chat with operator
        """
        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.ACTION}',
            method='get',
            params={
                'action': 'chat.start',
                'page-id': self.page_id,
                'auth-token': self.auth_token
            }
        )

    def make_file_upload_request(self):
        """
        Request to send visitor file. It should be stored and then added to delta list
        inside CHAT_MESSAGE `delta.data.text` field (serialized):
        u'[{
            guid":"4598ecc1ce874676ad07da804ac93e56",
            "filename":"file_200kb.txt",
            "content_type":"application/octet-stream",
            "client_content_type":"text/plain",
            "size":204800,"visitor_id":
            "f94c825708314ed280b3f1fecb8c321a"
        }]'
        """
        file_name = 'test.txt'
        file_path = os.path.join('/', 'home', 'k9173a', file_name)
        file_data = open(file_path, mode='r')
        content_type = 'text/plain'

        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.FILE_UPLOAD}',
            method='post',
            params={
                'page-id': self.page_id,
                'auth-token': self.auth_token
            },
            files={
                'webim_upload_file': (file_name, file_data, content_type)
            }
        )

    def make_chat_message_request(self):
        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.ACTION}',
            method='get',
            params={
                'action': 'chat.message',
                'page-id': self.page_id,
                'auth-token': self.auth_token,
                'message': 'This is message text!'
            }
        )

    def make_chat_file_message_request(self):
        """
        Sends file to chat.
        File is stored in the text field of Message object (dumped)
        """
        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.ACTION}',
            method='get',
            params={
                'action': 'chat.message',
                'page-id': self.page_id,
                'auth-token': self.auth_token,
                'kind': 'file_visitor',
                'message': json.dumps(self.file_data['data'])
            }
        )

    def make_delta_list_request(self):
        """
        Gets delta list with CHAT_MESSAGE delta and our file descriptor
        """
        return self.make_request(
            url=f'{WebimSdkSimulator.BASE_URL}{WebimSdkSimulator.Endpoint.DELTA}',
            method='get',
            params={
                'page-id': self.page_id,
                'auth-token': self.auth_token,
                'since': 1
            }
        )

    def prepare_visitor_ext(self):
        fields = {
            'phone': '+79998887766',
            'display_name': 'Иван',
            'id': str(uuid.uuid4()),
            'email': 'ivan@test.ru'
        }
        expires = 1681195621  # Tuesday, April 11, 2023 6:47:01 AM

        visitor_hash = self.get_provided_visitor_hash(fields=fields, expires=expires)

        return json.dumps({
            'hash': visitor_hash,
            'fields': fields,
            'expires': expires
        })

    def get_provided_visitor_hash(self, fields, expires):
        msg_parts = [fields[key] for key in sorted(fields.keys())]
        if expires:
            msg_parts.append(str(expires))
        msg = ''.join(msg_parts).encode('utf-8')

        return hmac.new(
            key=self.private_key.encode(),
            msg=msg,
            digestmod=hashlib.sha256  # account-config: provided_visitor_hash_algorithm
        ).hexdigest()


def main():
    simulator = WebimSdkSimulator()
    simulator.run()


if __name__ == '__main__':
    main()
