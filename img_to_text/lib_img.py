import cv2
import numpy as np


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
