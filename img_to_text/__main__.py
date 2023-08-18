# pip install easyocr
import easyocr
import cv2
import time

from enum import Enum
from .lib_img import crop_image, keep_color
from speakerpy.lib_helper import settings_selero
from speakerpy.lib_speak import Speaker


def logic_easyocr(image):
    # Преобразование в черно-белый формат
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = READER.readtext(
        grayscale_image,
        # Выводить близкие слова в одном элементе списка
        paragraph=True,
        # 0-Показывать только текст, 1-Показывать текст, и координаты найдено рамки, и процент точности
        detail=0,
    )
    return results


READER = easyocr.Reader(lang_list=["ru"], gpu=True)


class SettingGame(Enum):
    baldur_gate_3 = dict(
        bottom_percentage=20, width_percentage=19, color_hex="#ffffff", tolerance=180
    )


def orc_text(image, setting_game: SettingGame):
    """
    Распознать текст на изображение
    """
    st = setting_game.value

    # Вызов функции для обрезания изображения
    cropped_image = crop_image(
        image,
        bottom_percentage=st["bottom_percentage"],
        width_percentage=st["width_percentage"],
    )
    # Оставить только белый цвет субтитров
    bg_image = keep_color(
        cropped_image, color_hex=st["color_hex"], tolerance=st["tolerance"]
    )
    # # Сжатие изображения с потерями
    # scale_percent = 75  # Процент от исходного размера
    # width = int(bg_image.shape[1] * scale_percent / 100)
    # height = int(bg_image.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # resized_image = cv2.resize(bg_image, dim)

    # Распознавание текста
    res_orc_text = logic_easyocr(bg_image)
    return res_orc_text, bg_image


def filter_text(text: list[str]) -> str:
    print(f"до text={text}")
    if len(text) > 1:
        for i, t in enumerate(text):
            # ? Удалить тест про активацию Windows
            if t.find("Активаци") != -1:
                text[i] = ""

    # Удалить строку, содержащую "Активаци", если она есть
    # Удаляем имя персонажа который говорит
    text = ". ".join("".join(text).split(":")[1:])

    # Создание таблицы трансляции для замены цифр на слова
    translate_map = str.maketrans(
        {
            # Замена цифр на слова
            ord("1"): " один. ",
            ord("2"): " два. ",
            ord("3"): " три. ",
            ord("4"): " четыре. ",
            ord("5"): " пять. ",
            ord("6"): " шесть. ",
            ord("7"): " семь. ",
        }
    )

    # Применение таблицы трансляции
    text = text.translate(translate_map)

    # Замена неправильно распознанных слов
    text = text.replace("Уйш", "Уйти")

    return text.lstrip()


def main():
    dirs = "/home/denis/DISK/MyProject/speakerpy/img_to_text/"
    for i in [
        "atSfaAKvaN.jpg",
        "bg3_dx11_cKjW6fsU7z.jpg",
        "bg3_dx11_EBzPPTwp1B.jpg",
        "bg3_dx11_nLMRHBMzfX.jpg",
        "bg3_dx11_qs5wMkIhtj.jpg",
        "bg3_dx11_YuosNkKgoy.jpg",
    ]:
        # Прочитанное изображение
        input_image = cv2.imread(dirs + i)
        # >>>>>>>>>>>>>>>>>>>>>.
        print("Start: ")
        start_time = time.time()
        # Распознать текст на изображение
        res, resized_image = orc_text(
            input_image, setting_game=SettingGame.baldur_gate_3
        )
        print(f"END: execution_time={time.time() - start_time}")
        # >>>>>>>>>>>>>>>>>>>>>.
        # Сохранение обрезанного изображения
        cv2.imwrite(f"res_{i}", resized_image)
        # Удалить лишнее
        filter_res = filter_text(res)
        print(filter_res)

        # Озвучить текст
        sp = Speaker(**settings_selero["ru_man"]["sp"])
        sp.speak_stream(
            filter_res,
            sample_rate=settings_selero["ru_man"]["sample_rate"],
            speed=1.2,
        )


# input_image = cv2.imread(file)
# # Вызов функции для обрезания
# cropped_image = crop_image(input_image, bottom_percentage=20, width_percentage=19)
# # Сохранение обрезанного изображения
# cv2.imwrite("2_5.png", cropped_image)

main()
