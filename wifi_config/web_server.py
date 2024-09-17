from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from network_manager import NetworkManager

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_networks')
def handle_get_networks():
    networks = NetworkManager.get_wifi_networks()
    socketio.emit('networks_list', {'networks': networks})

@socketio.on('connect_wifi')
def handle_connect_wifi(data):
    ssid = data['ssid']
    password = data['password']
    success, message = NetworkManager.connect_to_wifi(ssid, password)
    if success:
        ip = NetworkManager.get_current_ip()
        socketio.emit('connection_result', {'success': True, 'ip': ip})
    else:
        socketio.emit('connection_result', {'success': False, 'error': message})

@socketio.on('exit_ap_mode')
def handle_exit_ap_mode():
    success, message = NetworkManager.exit_ap_mode()
    socketio.emit('exit_ap_result', {'success': success, 'message': message})

def run_server():
    socketio.run(app, host='0.0.0.0', port=80)