from flask import Blueprint

ws = Blueprint('ws', __name__)

sessions = dict()


@ws.route('/echo')
def echo_socket(socket):
    while not socket.closed:
        message = socket.receive()
        socket.send(message)


@ws.route('/chat')
def chat_socket(socket):

    alias = socket.receive()
    if alias in sessions:
        # duplicate ID
        raise ValueError("Duplicate alias")

    sessions[alias] = socket

    while not socket.closed:
        message = socket.receive()
        if message is None:
            continue
        print(f'New message by user {alias}: {message}')
        broadcast(alias, message)

    del sessions[alias]


def broadcast(user, message):
    for socket_owner, socket in sessions.items():
        if socket.closed:
            del sessions[socket_owner]
            return

        message_json = '{"user": "' + user + '", "text": "' + message + '"}'
        socket.send(message_json)


