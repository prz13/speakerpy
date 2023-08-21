import time

import cv2
import numpy as np
from gamesettings import SettingGame
from lib_img import game_orc

TEST_PHOTO = {
    "7sO8N6tAm6.jpg": {"name": "Иерле", "replic": "Тебе тут делать нечего."},
    "bg3_dx11_3Cpa0cbJTD.jpg": {
        "name": "Карлах",
        "replic": "Вечеринки у гоблинов гораздо веселее любых праздников во Вратах Балдура. Да и ваду тоже.",
    },
    "bg3_dx11_Ci8natY2ar.jpg": {
        "name": "Мрак",
        "replic": "Ты тоже за клеймом? Жрица говорит, нас всех надо пометить перед налетом.",
    },
    "bg3_dx11_kp0dK8UtUz.jpg": {
        "name": "Мрак",
        "replic": "Чтоб все, кому мы вмажем, были в курсе, что мы за Абсолют.",
    },
    "bg3_dx11_KuNt4VKWYP.jpg": {
        "name": "Карлах",
        "replic": "Вечеринки у гоблинов гораздо веселее любых праздников во Вратах Балдура. Да и ваду тоже.",
    },
    "bg3_dx11_T3HCDQ9vUm.jpg": {
        "name": "Эрна",
        "replic": "Не советую туда лезть, если не хочешь, чтоб твои кости аж до Врат Балдура долетели.",
    },
}


def main():
    dirs = "/home/denis/DISK/MyProject/speakerpy/eyeeaseai/img/"
    dirs_out = "/home/denis/DISK/MyProject/speakerpy/eyeeaseai/img_res/"
    for k, rais_value in TEST_PHOTO.items():
        # Прочитанное изображение
        input_image: np.ndarray = cv2.imread(dirs + k)
        # >>>>>>>>>>>>>>>>>>>>>.
        print("Start: ")
        start_time = time.time()
        # Распознать текст на изображение
        res_text, res_image = game_orc(
            input_image, setting_game=SettingGame.baldur_gate_3
        )
        print(f"END: execution_time={time.time() - start_time}")
        # >>>>>>>>>>>>>>>>>>>>>.
        if res_text != rais_value:
            raise KeyError(f"{res_text} != {rais_value}")

        # Сохранение итоговое изображения, на котором было произведено распознование текста
        cv2.imwrite(dirs_out + f"res_{k}", res_image)

        # Озвучить текст
        # sp = Speaker(**settings_selero["ru_man"]["sp"])
        # sp.speak_stream(
        #     filter_res,
        #     sample_rate=settings_selero["ru_man"]["sample_rate"],
        #     speed=1.2,
        # )


if __name__ == "__main__":
    main()
