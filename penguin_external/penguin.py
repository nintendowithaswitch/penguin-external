import time
import threading
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button
import vgamepad as vg

class Penguin:
    def __init__(self):
        self.delay = 0.680
        self.enabled = False
        self.key = 'f'
        self.gamepad = vg.VX360Gamepad()
        self.listener = None
        self.mouse_listener = None
        self.lock = threading.Lock()

    def fire(self):
        if not self.enabled:
            return

        with self.lock:
            current_delay = self.delay

        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()

        time.sleep(current_delay)

        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()

    def on_press(self, key):
        try:
            k = key.char.lower() if hasattr(key, 'char') and key.char else str(key).split('.')[-1]
        except:
            return
        if k == self.key and self.enabled:
            threading.Thread(target=self.fire, daemon=True).start()

    def start(self):
        if self.listener:
            return
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        if not self.mouse_listener:
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.mouse_listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        try:
            self.gamepad.reset()
            self.gamepad.update()
        except Exception:
            pass
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
            except Exception:
                pass
            self.mouse_listener = None

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
        try:
            if not self.enabled:
                return
            if button == Button.left:
                name = 'mouse_left'
            elif button == Button.middle:
                name = 'mouse_middle'
            elif button == Button.right:
                name = 'mouse_right'
            else:
                name = str(button).split('.')[-1]

            if name == self.key:
                threading.Thread(target=self.fire, daemon=True).start()
        except Exception:
            return
