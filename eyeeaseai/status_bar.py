import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path

import cv2
import keyboard
import numpy as np
import pyautogui


class StatusBar(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.label = tk.Label(self, text="Остановлено")
        self.label.pack()
        self.overrideredirect(True)
        self.geometry("+10+10")
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-alpha", 0.7)
        # self.wm_attributes("-transparentcolor", "white")

    def set_status(self, status):
        self.label.config(text=status)


def take_screenshot(status_bar):
    # Предполагая, что класс EyeEaseAi и его методы определены где-то в коде
    # ea = EyeEaseAi(setting_game=SettingGame.baldur_gate_3)

    while True:
        if not keyboard.is_pressed(
            "ctrl+alt+s"
        ):  # Замените на нужное сочетание клавиш для остановки
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            # res_text, res_image = ea.orc_img(screenshot_np)
            file_path = (
                Path(__file__).parent
                / "screenshots"
                / f"screenshots_{datetime.now().isoformat()}.png"
            )
            cv2.imwrite(str(file_path), screenshot_np)
            time.sleep(0.5)
        else:
            status_bar.set_status("Остановлено")
            break


def main():
    status_bar = StatusBar()
    status_bar.set_status("Запущено")

    t = threading.Thread(target=take_screenshot, args=(status_bar,))
    t.start()

    def stop():
        keyboard.press_and_release("ctrl+alt+s")
        status_bar.destroy()

    keyboard.add_hotkey(
        "ctrl+alt+q", stop
    )  # Замените на нужное сочетание клавиш для выхода

    status_bar.mainloop()
    t.join()


if __name__ == "__main__":
    main()
