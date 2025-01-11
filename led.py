import board
import digitalio
import threading
import time

class LED:
    SOLID = "SOLID"           # Normal operation, connected to WiFi
    FAST_BLINK = "FAST"       # AP Mode
    SLOW_BREATH = "BREATH"    # Attempting to connect
    OFF = "OFF"               # LED off

    def __init__(self, pin):
        self.pin = getattr(board, f'D{pin}')
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self._state = self.OFF
        self._running = True
        
        self.thread = threading.Thread(target=self._control_led, daemon=True)
        self.thread.start()

    def _fast_blink(self):
        self.led.value = not self.led.value
        return 0.2  # 200ms interval

    def _slow_breath(self):
        for i in range(0, 100, 2):
            if self._state != self.SLOW_BREATH:
                break
            # PWM simulation
            self.led.value = True
            time.sleep(i/10000.0)
            self.led.value = False
            time.sleep((100-i)/10000.0)
        return 0.01  # Return to control loop quickly

    def _solid(self):
        self.led.value = True
        return 0.1  # Check for state change every 100ms

    def _off(self):
        self.led.value = False
        return 0.1  # Check for state change every 100ms

    def _control_led(self):
        while self._running:
            # State machine for LED patterns
            if self._state == self.FAST_BLINK:
                sleep_time = self._fast_blink()
            elif self._state == self.SLOW_BREATH:
                sleep_time = self._slow_breath()
            elif self._state == self.SOLID:
                sleep_time = self._solid()
            else:  # OFF
                sleep_time = self._off()
            
            time.sleep(sleep_time)

    def set_state(self, state):
        """Change LED state to one of: SOLID, FAST_BLINK, SLOW_BREATH, OFF"""
        self._state = state

    def cleanup(self):
        """Clean up GPIO on exit"""
        self._running = False
        if self.thread.is_alive():
            self.thread.join()
        self.led.value = False