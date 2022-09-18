from flask import request
from waitress import serve
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, send
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='build', static_url_path='/')
app.debug = True
app.config['SECRET KEY'] = 'secret!'
# CORS(app)
socket = SocketIO(app, cors_allowed_origins='*')


@socket.on('connect')
def connect():
    print('\n *client connected* \n')


@socket.on('disconnect')
def disconnect():
    print('\n *client disconnected* \n')


@socket.on('post_message')
def post_message(new_message):
    with open('data.json', 'r+') as data_file:
        data = json.load(data_file)

        print(new_message)
        print(type(new_message))

        data['messages'].append(new_message)
        data_file.seek(0)
        json.dump(data, data_file, indent=4)

        # rest of the clients should request the messages again
        socket.emit('refresh', broadcast=True)

        return request.data


@socket.on('get_messages')
def get_messages():
    data_file = open('data.json')
    data = json.load(data_file)
    return data


@app.route('/', defaults={'path':''})
def index(path):
    return send_from_directory(app.static_folder, 'index.html')
    # return 'hello this is chat app server'


# @app.route("/messages", methods=['GET', 'POST'])
# def messages(msg=None):
#     if request.method == 'GET':
#         data_file = open(r'C:\Users\user\Desktop\Chat\server\data.json')
#         data = json.load(data_file)
#         return data

#     if request.method == 'POST':
#         with open(r'C:\Users\user\Desktop\Chat\server\data.json', 'r+') as data_file:
#             data = json.load(data_file)

#             new_message = json.loads(request.data)
#             print(new_message)
#             print(type(new_message))

#             data['messages'].append(new_message)
#             data_file.seek(0)
#             json.dump(data, data_file, indent=4)
#             send('REFRESH', broadcast=True)
#             return request.data

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000)
