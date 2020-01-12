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
    sessions[alias] = socket

    while not socket.closed:
        message = socket.receive()
        print(f'New message by user {alias}: {message}')
        broadcast(alias, message)

    del sessions[alias]


def broadcast(user, message):
    for socket_owner, socket in sessions.items():
        if socket.closed:
            del sessions[socket_owner]
            return

        socket.send(f'{user}: {message}')


