from flask import Flask, render_template, request
from flask_socketio import SocketIO
from wifi_config.network_manager import NetworkManager
import threading
from logger import logger
from time import sleep
import os

# ------------------------------------------- #
# ************* Global Variables ************ #
# ------------------------------------------- #

server_running = False
server_thread = None
PORT = 80


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('connect')
def test_connect():
    logger.info("[web_server.py][Status] Client connected")

@socketio.on('disconnect')
def test_disconnect():
    logger.info("[web_server.py][Status] Client disconnected")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/js/socket.io.js')
def serve_socketio_js():
    return app.send_static_file('js/socket.io.js')

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return app.send_static_file(f'images/{filename}')




@socketio.on('connect_wifi')
def handle_connect_wifi(data):
    ssid = data['ssid']
    password = data['password']

    success, message = NetworkManager.connect_to_wifi(ssid, password)
    
    logger.debug(f"[web_server.py][Status] Connection success: {success}")
    logger.debug(f"[web_server.py][Status] Connection message: {message}")
    
    if success:
        ip = NetworkManager.get_current_ip()
        logger.info(f'[web_server.py][Result] The current IP is: {ip}')
        socketio.emit('connection_result', {'success': True, 'ip': ip})
        # Start a new thread to shut down the server
        threading.Thread(target=shutdown_server).start()
    else:
        logger.error(f'[web_server.py][Result] Connection failed: {message}')
        socketio.emit('connection_result', {'success': False, 'error': message})


def run_server():
    global server_running
    server_running = True
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False, log_output=False, allow_unsafe_werkzeug=True)


def stop_server():
    global server_running, server_thread
    if server_running:
        server_running = False
        logger.info("[web_server.py][Status] Stopping web server...")
        socketio.stop()
        logger.info("[web_server.py][Result] Web server stopped.")

def shutdown_server():
    stop_server()
    sleep(5)
    # # Force exit the server thread
    os._exit(0)
