from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import network_manager

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_networks')
def handle_get_networks():
    networks = network_manager.NetworkManager.get_wifi_networks()
    socketio.emit('networks_list', {'networks': networks})

@socketio.on('connect_wifi')
def handle_connect_wifi(data):
    ssid = data['ssid']
    password = data['password']
    success, message = network_manager.NetworkManager.connect_to_wifi(ssid, password)
    if success:
        ip = network_manager.NetworkManager.get_current_ip()
        socketio.emit('connection_result', {'success': True, 'ip': ip})
    else:
        socketio.emit('connection_result', {'success': False, 'error': message})

def run_server():
    socketio.run(app, host='10.10.1.1', port=80)