from pynput.mouse import Button, Controller as MController, Listener as MListener
from pynput.keyboard import Key, Controller as KController, Listener as KListener

class Mouse:
    def __init__(self):
        self.is_stop = False
        self.controller = MController()

    def click(self, x, y, times=1):
        # self.mouse.position = (x, y)
        self.is_stop = False
        for i in range(times):
            if self.is_stop is False:
                self.controller.click(Button.left)

    def stop(self):
        self.is_stop = True

    @property
    def on_click(self):
        return

    @on_click.setter
    def on_click(self, handler):
        with MListener(on_click=handler) as listener:
            listener.join()


class Keyboard:
    def __init__(self):
        self.is_stop = False
        self.controller = KController

    def press_release(self, key, times=1):
        self.is_stop = False
        for i in range(times):
            if self.is_stop is False:
                self.press(key)
                self.release(key)

    def press(self, key):
        self.controller.press(key)

    def release(self, key):
        self.controller.release(key)

    @property
    def on_press(self):
        return

    @on_press.setter
    def on_press(self, handler):
        with KListener(on_press=handler) as listener:
            listener.join()


def on_click(x, y, button, pressed):
    print('mouse clicked')

def on_press(key):
    global mouse
    global esc_count

    if key is not Key.esc:
        esc_count = 0

    if key is Key.esc:
        # double press esc, then exit program
        if esc_count is 1:
            return False
        else:
            mouse.stop()
            # mouse.on_click = None
            print('mouse stopped')
        esc_count += 1
    elif key is Key.shift:
        mouse.click(1541, 787, 100)
        print('mouse started')

## Global Variables ##
mouse = Mouse()
keyboard = Keyboard()

esc_count = 0
######################

def main():
    global keyboard
    global mouse

    keyboard.on_press = on_press
    # mouse.on_click = on_click

if __name__ == '__main__':
    main()
