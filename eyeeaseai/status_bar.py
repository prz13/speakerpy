from collections import deque
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path

import cv2
import keyboard
import numpy as np
import pyautogui
from eyeeaseai.gamesettings import SettingGame

from eyeeaseai.lib_img import EyeEaseAi

# pip install opencv-python keyboard pyautogui silero pytesseract


class StatusBar(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Остановлено")
        self.label.pack()
        self.overrideredirect(True)
        self.geometry("+10+10")
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")

    def set_status(self, status):
        self.label.config(text=status)


dir_scrinshot = Path(__file__).parent / "screenshots"
is_running = False


def take_screenshot(status_bar):
    global is_running
    ea = EyeEaseAi(setting_game=SettingGame.baldur_gate_3)

    i = 0
    skeep_list = deque()
    while True:
        if is_running:
            print(i)
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            res_text, res_image = ea.orc_img(screenshot_np)
            if res_text:
                skeep_list.append(res_text["replica"])
                status_bar.set_status(f"Запущено:\n{skeep_list}")
                ea.speak(skeep_list.popleft())
            #
            # file_path = dir_scrinshot / f"screenshots_{i}.png"
            # cv2.imwrite(str(file_path), screenshot_np)
            #
            time.sleep(0.5)
            #
            i += 1


def toggle_screenshot(status_bar):
    global is_running
    is_running = not is_running
    status_bar.set_status("Запущено" if is_running else "Остановлено")


def main():
    global is_running
    status_bar = StatusBar()
    status_bar.set_status("Остановлено")

    keyboard.add_hotkey("ctrl+alt+s", lambda: toggle_screenshot(status_bar))

    t = threading.Thread(target=take_screenshot, args=(status_bar,), daemon=True)
    t.start()

    def stop():
        keyboard.press_and_release("ctrl+alt+s")
        status_bar.destroy()

    keyboard.add_hotkey("ctrl+alt+q", stop)

    status_bar.mainloop()
    t.join()


if __name__ == "__main__":
    main()
