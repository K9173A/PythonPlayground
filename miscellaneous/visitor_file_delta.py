import datetime
import json
import os

import requests


def print_response(response):
    print '#' * 80
    print json.dumps(response, indent=4, sort_keys=True)
    print '#' * 80


def main():
    # Node: increase DELTA_LIVE_PERIOD to 3000 to catch deltas before their removal

    base_url = 'https://dev.webimdev.ru'
    action_endpoint_path = '/l/v/m/action'
    delta_endpoint_path = '/l/v/m/delta'
    visitor_file_upload_path = '/l/v/m/upload'

    random_device_id = 'device-id/' + datetime.datetime.now().ctime()
    random_push_token = 'token/' + datetime.datetime.now().ctime()

    # Initializing client
    init_response = requests.get(
        url=base_url + delta_endpoint_path,
        params={
            'device-id': random_device_id,  # device-id is being created on event=init only
            'event': 'init',
            'respond-immediately': 1,  # used in `if since != self.get_current_revision() or waiter.request_handler.get_argument('respond-immediately', 'false') == 'true'`
            'push-token': random_push_token,
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
            }
        }
    )

    init_response.raise_for_status()
    init_response_data = init_response.json()
    if init_response_data.get('error'):
        print init_response_data['error']
        return
    else:
        print_response(init_response_data)

    page_id = init_response_data['fullUpdate']['pageId']
    auth_token = init_response_data['fullUpdate']['authToken']

    # Starting chat with operator

    response_chat_start = requests.get(
        url=base_url + action_endpoint_path,
        params={
            'action': 'chat.start',
            'page-id': page_id,
            'auth-token': auth_token
        }
    )

    response_chat_start.raise_for_status()
    response_chat_start_data = response_chat_start.json()
    if response_chat_start_data.get('error'):
        print response_chat_start_data['error']
        return
    else:
        print_response(response_chat_start_data)

    file_name = 'filezzz_200kb.txt'
    file_path = os.path.join('/', 'home', 'k9173a', file_name)

    # Sending file. It should be stored and then added to delta list inside CHAT_MESSAGE `delta.data.text` field (serialized):
    # u'[{
    #     "guid":"4598ecc1ce874676ad07da804ac93e56",
    #     "filename":"file_200kb.txt",
    #     "content_type":"application/octet-stream",
    #     "client_content_type":"text/plain",
    #     "size":204800,"visitor_id":
    #     "f94c825708314ed280b3f1fecb8c321a"
    # }]'
    upload_file_response = requests.post(
        url=base_url + visitor_file_upload_path,
        params={
            'page-id': page_id,
            'auth-token': auth_token
        },
        files={
            'webim_upload_file': (file_name, open(file_path, mode='r'), 'text/plain')  # (file_name, file_data, content_type)
        }
    )

    upload_file_response.raise_for_status()
    upload_file_response_data = upload_file_response.json()
    if upload_file_response_data.get('error'):
        print upload_file_response_data['error']
        return
    else:
        print_response(upload_file_response_data)

    # File is stored in the text field of Message object (dumped)
    chat_message_response = requests.get(
        url=base_url + action_endpoint_path,
        params={
            'action': 'chat.message',
            'page-id': page_id,
            'auth-token': auth_token,
            'kind': 'file_visitor',
            'message': json.dumps(upload_file_response_data['data'])
        }
    )

    chat_message_response.raise_for_status()
    chat_message_response_data = chat_message_response.json()
    if chat_message_response_data.get('error'):
        print chat_message_response_data['error']
        return
    else:
        print_response(chat_message_response_data)

    # Getting delta list with CHAT_MESSAGE delta and our file descriptor
    delta_list_response = requests.get(
        url=base_url + delta_endpoint_path,
        params={
            'page-id': page_id,
            'auth-token': auth_token,
            'since': 1
        }
    )

    delta_list_response.raise_for_status()
    delta_list_response_data = delta_list_response.json()
    if delta_list_response_data.get('error'):
        print delta_list_response_data['error']
        return
    else:
        print_response(delta_list_response_data)


if __name__ == '__main__':
    main()
