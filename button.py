import board
import digitalio
import threading
import time
import subprocess

class Button:
    def __init__(self, pin, debounce_time=0.01, long_press_time=5):
        self.pin = getattr(board, f'D{pin}')
        self.button = digitalio.DigitalInOut(self.pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        
        self.debounce_time = debounce_time
        self.long_press_time = long_press_time
        
        self.last_state = self.button.value
        self.last_change_time = time.monotonic()
        self.press_start_time = None
        
        self.thread = threading.Thread(target=self._check_button, daemon=True)
        self.thread.start()

    def _check_button(self):
        while True:
            current_state = self.button.value
            current_time = time.monotonic()
            
            if current_state != self.last_state and (current_time - self.last_change_time) > self.debounce_time:
                if current_state:  # Button released
                    if self.press_start_time:
                        press_duration = current_time - self.press_start_time
                        if press_duration >= self.long_press_time:
                            self._on_long_press()
                        else:
                            self._on_short_press()
                        self.press_start_time = None
                else:  # Button pressed
                    self.press_start_time = current_time
                
                self.last_state = current_state
                self.last_change_time = current_time
            
            time.sleep(0.001)  # Check every 1 ms

    def _on_short_press(self):
        print("Short press detected")

    def _on_long_press(self):
        print("\nLong press detected")
        self._run_shell_command()

    def _run_shell_command(self):
        try:
            result = subprocess.run(["echo", "Long press action executed"], capture_output=True, text=True)
            print(f"Shell command output: {result.stdout}")
        except Exception as e:
            print(f"Error running shell command: {e}")