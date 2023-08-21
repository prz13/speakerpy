import re

import cv2
import numpy as np
import pytesseract
from gamesettings import SettingGame


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


def recognize_text_with_settings(image: np.ndarray, setting_game: SettingGame):
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

    r_img = in_image
    # Распознавание текста
    res_orc_text = perform_ocr(r_img)
    return res_orc_text, r_img


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
        for x in re.finditer(r"(?P<name>[\w\d]+): (?P<replic>(?:.(?!\.\\n))+.)", text)
    ]
    if len(text_obj) > 1:
        raise KeyError("Не может быть больше одной реплики")
    text_obj = text_obj[0]

    replic = text_obj["replic"]

    # Применение таблицы трансляции
    replic = replic.translate(
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
    replic = replic.replace("Уйш", "Уйти")

    text_obj["replic"] = replic.strip()
    return text_obj
