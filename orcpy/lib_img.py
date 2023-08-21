import cv2
import numpy as np
import pytesseract
import re
import cv2

from gamesettings import SettingGame


def crop_image(image, bottom_percentage=25, width_percentage=10):
    """Функция для обрезания изображения"""
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


def keep_color(image, color_hex="#ffffff", tolerance=90):
    """
    Функция которая оставляет на изображениям только указанный цвет
    (возможно указать погрешность цвета который можно отсавить в аргумент tolerance)

    color_hex: Цвет, который нужно оставить
    tolerance: Допустимое отклонение от заданного цвета
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


def remove_color(image, color_hex="#ffffff", tolerance=90):
    """
    Функция, которая удаляет из изображения указанный цвет
    (возможно указать погрешность цвета, который можно удалить, в аргументе tolerance)

    color_hex: Цвет, который нужно удалить
    tolerance: Допустимое отклонение от заданного цвета
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


def invert_colors(image):
    """
    Функция, которая инвертирует все цвета на изображении
    """
    # Инвертирование цветов с помощью вычитания значений каждого пикселя из 255
    inverted_image = 255 - image

    return inverted_image


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
        cropped_image, color_hex=st["keep_color_hex"], tolerance=st["keep_tolerance"]
    )

    # Инвертировать белый цвет в черный, потому что OCR чаще обучается на черном тексте а не на белом
    in_image = invert_colors(bg_image)

    r_img = in_image
    # Распознавание текста
    res_orc_text = logic_recognize(r_img)
    return res_orc_text, r_img


def filter_text(text: str) -> str:
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


def logic_recognize(image):
    """Распознать текс на изображение"""
    results = pytesseract.image_to_string(image, lang="rus")
    return results
