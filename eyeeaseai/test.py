import time

import cv2
import numpy as np
from gamesettings import SettingGame
from lib_img import Dialog, EyeEaseAi
from pathlib import Path

TEST_PHOTO: dict[str, Dialog] = {
    "7sO8N6tAm6.jpg": {"name": "Иерле", "replica": "Тебе тут делать нечего."},
    "bg3_dx11_3Cpa0cbJTD.jpg": {
        "name": "Карлах",
        "replica": "Вечеринки у гоблинов гораздо веселее любых праздников во Вратах Балдура. Да и ваду тоже.",
    },
    "bg3_dx11_Ci8natY2ar.jpg": {
        "name": "Мрак",
        "replica": "Ты тоже за клеймом? Жрица говорит, нас всех надо пометить перед налетом.",
    },
    "bg3_dx11_kp0dK8UtUz.jpg": {
        "name": "Мрак",
        "replica": "Чтоб все, кому мы вмажем, были в курсе, что мы за Абсолют.",
    },
    "bg3_dx11_KuNt4VKWYP.jpg": {
        "name": "Карлах",
        "replica": "Вечеринки у гоблинов гораздо веселее любых праздников во Вратах Балдура. Да и ваду тоже.",
    },
    "bg3_dx11_T3HCDQ9vUm.jpg": {
        "name": "Эрна",
        "replica": "Не советую туда лезть, если не хочешь, чтоб твои кости аж до Врат Балдура долетели.",
    },
    "screenshots_20.png": {
        "name": "Шэдоухарт",
        "replica": "Идем прямиком в лапы гоблинского боевого клана... Многие сочли бы, что мы сошли с ума. Вот настолько мы в отчаянии, да.",
    },
}


def main():
    dirs = Path(__file__).parent / "img"
    dirs_out = Path(__file__).parent / "img_res"

    ea = EyeEaseAi(setting_game=SettingGame.baldur_gate_3)
    for k, rais_value in TEST_PHOTO.items():
        # Прочитанное изображение
        input_image: np.ndarray = cv2.imread(str(dirs / k))
        # >>>>>>>>>>>>>>>>>>>>>.
        print("Start: ")
        start_time = time.time()
        # Распознать текст на изображение
        res_text, res_image = ea.orc_img(input_image)
        print(f"END: execution_time={time.time() - start_time}")
        # >>>>>>>>>>>>>>>>>>>>>.
        # Сохранение итоговое изображения, на котором было произведено распознование текста
        cv2.imwrite(str(dirs_out / f"res_{k}"), res_image)

        if res_text != rais_value:
            raise KeyError(f"{res_text} != {rais_value}")


if __name__ == "__main__":
    # main()
    ea = EyeEaseAi(setting_game=SettingGame.baldur_gate_3)
    print("start")
    ea.speak(
        "Не советую туда лезть, если не хочешь, чтоб твои кости аж до Врат Балдура долетели."
    )
    ea.speak("Ты тоже за клеймом? Жрица говорит, нас всех надо пометить перед налетом")
    print("End")

    # take_screenshot()
