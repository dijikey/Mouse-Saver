import pyautogui as gui
import keyboard as key
from pynput import mouse
from time import sleep, time


class Screensaver:
    def __init__(self, speed: tuple = (200, 200), timeout: int = 120):
        self.screen_width, self.screen_height = gui.size()
        self.center_x, self.center_y = [self.screen_width // 2, self.screen_height // 2]
        self.speed_x, self.speed_y = speed
        self.timeout = timeout
        self.last_move = time()
        self.condition = [False, True]

        self.listener = mouse.Listener(on_move=self.on_move)

    def on_move(self, x, y):
        self.last_move = time()

    def check_timeout(self):
        current_time = time()
        if current_time - self.last_move >= self.timeout and self.condition[1]:
            self.condition[1] = False
            self.run()

    def run(self):
        self.condition[0] = True
        gui.moveTo(self.center_x, self.center_y)
        try:
            while self.condition[0]:
                self.center_x += self.speed_x
                self.center_y += self.speed_y

                if self.center_x <= 0 or self.center_x >= self.screen_width:
                    self.speed_x = -self.speed_x

                if self.center_y <= 0 or self.center_y >= self.screen_height:
                    self.speed_y  = -self.speed_y

                gui.moveTo(self.center_x, self.center_y, 1, _pause=False)
                if key.is_pressed('space'):
                    self.condition[0] = False
                    self.condition[1] = True
                    self.listener.start()
        except gui.FailSafeException:
            self.condition[0] = False
            self.listener.start()


if __name__ == '__main__':
    root = Screensaver(timeout=5)
    while True:
        root.check_timeout()
        sleep(1)
