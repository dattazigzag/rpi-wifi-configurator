from flask import Flask, render_template, request
from flask_socketio import SocketIO
from wifi_config.network_manager import NetworkManager
from logger import logger
from time import sleep
from led import LED
status_led: LED = None  # Type hint
from led import LED
status_led: LED = None  # Type hint

# ------------------------------------------- #
# ************* Global Variables ************ #
# ------------------------------------------- #

server_running = False
server_thread = None
PORT = 8080
PORT = 8080
is_ap_mode = False
last_connection_success = False


# ------------------------------------------- #
# ************* Application_init ************ #
# ------------------------------------------- #

app = Flask(__name__)
socketio = SocketIO(app)

def init_app(led_instance):
    global status_led
    status_led = led_instance
    return app


# ------------------------------------------- #
# ********** General Conn Handlers ********** #
# ------------------------------------------- #

@socketio.on('connect')
def test_connect():
    logger.info("[web_server.py][Status] Client connected")

@socketio.on('disconnect')
def test_disconnect():
    logger.info("[web_server.py][Status] Client disconnected")


# ------------------------------------------- #
# **************** Router Func ************** #
# ------------------------------------------- #

@app.route('/')
def index():
    # Note: TBT: In the new method suggested by ai these global vars are removed, why?
    global is_ap_mode, last_connection_success
    if is_ap_mode and not last_connection_success:
        return render_template('index.html')
    else:
        return render_template('general.html')


# ------------------------------------------- #
# ********** File Serving Routers *********** #
# ------------------------------------------- #

@app.route('/static/js/socket.io.js')
def serve_socketio_js():
    return app.send_static_file('js/socket.io.js')

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return app.send_static_file(f'images/{filename}')


@socketio.on('connect_wifi')
def handle_connect_wifi(data):
    global is_ap_mode, last_connection_success
    ssid = data['ssid']
    password = data['password']
    
    # Set LED to breathing while attempting connection
    status_led.set_state(LED.SLOW_BREATH)
    
    logger.debug(f"[web_server.py][Status] Attempting to connect to SSID: {ssid}")
    
    # Set LED to breathing while attempting connection
    status_led.set_state(LED.SLOW_BREATH)
    
    logger.debug(f"[web_server.py][Status] Attempting to connect to SSID: {ssid}")

    success, message = NetworkManager.connect_to_wifi(ssid, password)
    
    logger.debug(f"[web_server.py][Status] Connection success: {success}")
    logger.debug(f"[web_server.py][Status] Connection message: {message}")
    
    if success:
        ip = NetworkManager.get_current_ip()
        logger.info(f'[web_server.py][Result] The current IP is: {ip}')
        socketio.emit('connection_result', {'success': True, 'ip': ip})
        is_ap_mode = False
        last_connection_success = True
        switch_to_normal_mode()
        status_led.set_state(LED.SOLID)
        sleep(2)
        status_led.set_state(LED.OFF)
        switch_to_normal_mode()
        status_led.set_state(LED.SOLID)
        sleep(2)
        status_led.set_state(LED.OFF)
    else:
        logger.error(f'[web_server.py][Result] Connection failed: {message}')
        socketio.emit('connection_result', {'success': False, 'error': message})
        last_connection_success = False
        status_led.set_state(LED.FAST_BLINK)


def run_server():
    global server_running
    server_running = True
    socketio.run(app, host='0.0.0.0', port=PORT, debug=False, log_output=False, allow_unsafe_werkzeug=True)

def stop_server():
    global server_running
    if server_running:
        server_running = False
        logger.info("[web_server.py][Status] Stopping web server...")
        socketio.stop()
        sleep(2)
        logger.info("[web_server.py][Result] Web server stopped.")


def reset_wifi_state():
    global is_ap_mode, last_connection_success
    is_ap_mode = True
    last_connection_success = False
    logger.info("[web_server.py][Status] WiFi state reset. Ready for new configuration.")


def switch_to_ap_mode():
    is_ap_mode = True
    logger.info("[web_server.py][Status] Switched to AP mode")

def switch_to_normal_mode():
    global is_ap_mode, last_connection_success
    is_ap_mode = False
    last_connection_success = True
    logger.info("[web_server.py][Status] Switched to normal mode")