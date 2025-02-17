from datetime import datetime
import re
import sys
from pathlib import Path
import time
from typing import TypedDict

import cv2
import numpy as np

# pip install pyautogui
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from gamesettings import SettingGame

sys.path.insert(0, str(Path(__file__).parent.parent))


from speakerpy.lib_helper import settings_selero
from speakerpy.lib_speak import Speaker


def crop_image_percentage(image: np.ndarray, bottom_percentage=25, width_percentage=10):
    """
    Обрезает изображение с указанными процентами снизу и с боков.

    Args:
        image (numpy.ndarray): Исходное изображение.
        bottom_percentage (int, optional): Процент обрезания снизу. По умолчанию 25.
        width_percentage (int, optional): Процент обрезания с боков. По умолчанию 10.

    Returns:
        numpy.ndarray: Обрезанное изображение.
    """
    # Получение высоты и ширины изображения
    height, width = image.shape[:2]

    # Вычисление высоты обрезанной нижней части
    cropped_height = int(height * bottom_percentage / 100)

    # Вычисление ширины обрезанных сторон
    cropped_width = int(width * width_percentage / 100)

    # Обрезание нижней части и сторон изображения
    cropped_image = image[
        height - cropped_height :, cropped_width : width - cropped_width
    ]

    return cropped_image


def extract_color(image: np.ndarray, color_hex="#ffffff", tolerance=90):
    """
    Оставляет только указанный цвет на изображении с заданной погрешностью.

    Args:
        image (numpy.ndarray): Исходное изображение.
        color_hex (str, optional): Цвет в HEX-формате (например, "#ffffff").
        tolerance (int, optional): Допустимое отклонение цвета. По умолчанию 90.

    Returns:
        numpy.ndarray: Изображение с оставленным цветом.
    """
    # Преобразование цвета из HEX в RGB
    color = tuple(int(color_hex[i : i + 2], 16) for i in (1, 3, 5))

    # Определение нижней и верхней границы для маски с учетом допустимого отклонения
    lower_bound = np.array([max(c - tolerance, 0) for c in color], dtype=np.uint8)
    upper_bound = np.array([min(c + tolerance, 255) for c in color], dtype=np.uint8)

    # Построение маски для определенного цвета
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Применение маски к изображению
    result = cv2.bitwise_and(image, image, mask=mask)

    # Возвращение результата
    return result


def remove_color_tolerant(image: np.ndarray, color_hex="#ffffff", tolerance=90):
    """
    Удаляет указанный цвет из изображения с заданной погрешностью.

    Args:
        image (numpy.ndarray): Исходное изображение.
        color_hex (str, optional): Цвет в HEX-формате (например, "#ffffff").
        tolerance (int, optional): Допустимое отклонение цвета. По умолчанию 90.

    Returns:
        numpy.ndarray: Изображение без указанного цвета.
    """
    # Преобразование цвета из HEX в RGB
    color = tuple(int(color_hex[i : i + 2], 16) for i in (1, 3, 5))

    # Определение нижней и верхней границы для маски с учетом допустимого отклонения
    lower_bound = np.array([max(c - tolerance, 0) for c in color], dtype=np.uint8)
    upper_bound = np.array([min(c + tolerance, 255) for c in color], dtype=np.uint8)

    # Построение маски для определенного цвета
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Инвертирование маски, чтобы убрать нужный цвет
    inverted_mask = cv2.bitwise_not(mask)

    # Применение инвертированной маски к изображению
    result = cv2.bitwise_and(image, image, mask=inverted_mask)

    # Возвращение результата
    return result


def invert_image_colors(image: np.ndarray):
    """
    Инвертирует цвета на изображении.

    Args:
        image (numpy.ndarray): Исходное изображение.

    Returns:
        numpy.ndarray: Инвертированное изображение.
    """
    # Инвертирование цветов с помощью вычитания значений каждого пикселя из 255
    inverted_image = 255 - image

    return inverted_image


def perform_ocr(image: np.ndarray):
    """
    Распознает текст на изображении с помощью библиотеки Tesseract.

    Args:
        image (numpy.ndarray): Исходное изображение.

    Returns:
        str: Распознанный текст.
    """
    results = pytesseract.image_to_string(image, lang="rus")
    return results


def recognize_text_with_settings(
    image: np.ndarray, setting_game: SettingGame
) -> tuple[str, np.array]:
    """
    Распознает текст на изображении с заданными настройками игры.

    Args:
        image (numpy.ndarray): Исходное изображение с текстом.
        setting_game (SettingGame): Настройки игры.

    Returns:
        tuple: Кортеж из распознанного текста и изображения после обработки.
    """
    st = setting_game.value

    # Вызов функции для обрезания изображения
    cropped_image = crop_image_percentage(
        image,
        bottom_percentage=st["bottom_percentage"],
        width_percentage=st["width_percentage"],
    )
    # Оставить только белый цвет субтитров
    bg_image = extract_color(
        cropped_image, color_hex=st["keep_color_hex"], tolerance=st["keep_tolerance"]
    )

    # Инвертировать белый цвет в черный, потому что OCR чаще обучается на черном тексте а не на белом
    in_image = invert_image_colors(bg_image)

    res_img = in_image
    # Распознавание текста
    res_orc_text = perform_ocr(res_img)
    return res_orc_text, res_img


def extract_character_dialogue(text: str) -> str:
    """
    Фильтрует и обрабатывает распознанный текст, оставляя только реплику персонажа.

    Args:
        text (str): Распознанный текст.

    Returns:
        str: Обработанная реплика персонажа.
    """
    # print(f"до text={text}")
    # Взять из текста только реплику персонажа
    text_obj = [
        x.groupdict()
        for x in re.finditer(
            r"(?P<name>[\w\d]+): (?P<replica>(?:.(?!\.\t))+.)", text.replace("\n", "\t")
        )
    ]
    if len(text_obj) > 1:
        raise KeyError("Не может быть больше одной реплики")
    if len(text_obj) == 0:
        return None

    text_obj = text_obj[0]

    replica = text_obj["replica"]
    replica = replica.replace("\t", " ")

    # Применение таблицы трансляции
    replica = replica.translate(
        # Создание таблицы трансляции для замены цифр на слова
        str.maketrans(
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
    )

    # Замена неправильно распознанных слов
    replica = replica.replace("Уйш", "Уйти")

    # Добавить в конец точку
    replica += "."
    text_obj["replica"] = replica.strip()
    return text_obj


# def take_screenshot():
#     """Делать скриншоты


#     Для Linux нужно дополнительно установить `sudo apt-get install scrot`
#     """
#     ea = EyeEaseAi(setting_game=SettingGame.baldur_gate_3)

#     while True:
#         screenshot = pyautogui.screenshot()
#         screenshot_np = np.array(screenshot)
#         # res_text, res_image = ea.orc_img(
#         #     screenshot_np
#         # )  # Передача скриншота в функцию orc_img
#         cv2.imwrite(
#             str(
#                 Path(__file__).parent
#                 / "screenshots"
#                 / f"screenshots_{datetime.now().isoformat()}.png"
#             ),
#             screenshot_np,
#         )
#         # Пауза в 0.5 секунды
#         time.sleep(0.5)


class Dialog(TypedDict):
    name: str
    replica: str


class EyeEaseAi:
    def __init__(self, setting_game=SettingGame) -> None:
        # Прошлое значение распознавание текста
        # Оно нужно для того чтобы повторно, еденивроенно не озвучивать текст
        self.last_res_orc: Dialog = None
        self.speaker_obj = Speaker(**settings_selero["ru_man"]["sp"])
        self.sample_rate = settings_selero["ru_man"]["sample_rate"]
        self.setting_game = setting_game

    def orc_img(self, image: np.ndarray) -> tuple[Dialog, np.array]:
        """Распознать текст на изображение

        return: Распознанный текст
        """
        res_text, res_image = recognize_text_with_settings(
            image, setting_game=self.setting_game
        )
        # Удалить лишние символы из ответа
        filter_dialog = extract_character_dialogue(res_text)

        # Если распознан новый текст, то возвратим его для дальнейшего озвучивания
        if filter_dialog and self.last_res_orc != filter_dialog:
            return filter_dialog, res_image
        else:
            return None, None

    def speak(self, text: str):
        """Озвучить текст"""
        self.speaker_obj.speak_stream(
            text,
            sample_rate=self.sample_rate,
            speed=1.2,
        )
