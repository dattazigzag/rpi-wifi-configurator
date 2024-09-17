from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from wifi_config.network_manager import NetworkManager

app = Flask(__name__)
socketio = SocketIO(app)

server_running = False


@app.route('/')
def index():
    return render_template('index.html')

# Ensure the socket.io.js file is served
@app.route('/static/js/socket.io.js')
def serve_socketio_js():
    return app.send_static_file('js/socket.io.js')

# Ensure the background image file is served
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return app.send_static_file(f'images/{filename}')


@socketio.on('connect_wifi')
def handle_connect_wifi(data):
    ssid = data['ssid']
    password = data['password']
    success, message = NetworkManager.connect_to_wifi(ssid, password)
    if success:
        ip = NetworkManager.get_current_ip()
        socketio.emit('connection_result', {'success': True, 'ip': ip})
        stop_server()  # Stop the server after successful connection
        print(f'The current IP is: {ip}')
    else:
        socketio.emit('connection_result', {'success': False, 'error': message})



def run_server():
    global server_running
    server_running = True
    socketio.run(app, host='0.0.0.0', port=80, debug=False)


def stop_server():
    global server_running
    server_running = False
    socketio.stop()
    print("Web server stopped.")