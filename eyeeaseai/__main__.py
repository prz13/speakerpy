# from speakerpy.lib_helper import settings_selero
# from speakerpy.lib_speak import Speaker


# input_image = cv2.imread(file)
# # Вызов функции для обрезания
# cropped_image = crop_image(input_image, bottom_percentage=20, width_percentage=19)
# # Сохранение обрезанного изображения
# cv2.imwrite("2_5.png", cropped_image)

# from PIL import Image


# def draw_text_boxes(image_path, color=(128, 0, 128), thickness=2, threshold=60):
#     image = cv2.imread(image_path)
#     pil_image = Image.open(image_path)
#     data = pytesseract.image_to_data(
#         pil_image, lang="rus", output_type=pytesseract.Output.DICT
#     )
#     print()
#     # lines = []
# line = []
# prev_y = 0
# for i in range(len(data["level"])):
#     if int(data["conf"][i]) > 0:  # Исключаем пустые или нераспознанные области
#         x, y, w, h = (
#             data["left"][i],
#             data["top"][i],
#             data["width"][i],
#             data["height"][i],
#         )
#         if prev_y and abs(y - prev_y) > threshold:
#             lines.append(line)
#             line = []
#         line.append((x, y, w, h))
#         prev_y = y

# if line:
#     lines.append(line)

# for line in lines:
#     x1 = min([box[0] for box in line])
#     y1 = min([box[1] for box in line])
#     x2 = max([box[0] + box[2] for box in line])
#     y2 = max([box[1] + box[3] for box in line])

#     cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

# cv2.imwrite("cropped_text.jpg", image)


# image_path = (
#     "/home/denis/DISK/MyProject/speakerpy/eyeeaseai/img_res/res_bg3_dx11_Ci8natY2ar.jpg"
# )
# draw_text_boxes(image_path)


# import cv2
# import pytesseract
# from PIL import Image


# def crop_text(image_path):
#     # Загрузка изображения
#     image = cv2.imread(image_path)
#     # Преобразование изображения в оттенки серого
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Бинаризация изображения для выделения текста
#     _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     # Нахождение контуров на бинаризованном изображении
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Определение границ текста
#     x_min, y_min, x_max, y_max = float("inf"), float("inf"), 0, 0
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         x_min = min(x_min, x)
#         y_min = min(y_min, y)
#         x_max = max(x_max, x + w)
#         y_max = max(y_max, y + h)

#     # Обрезка изображения по найденным границам
#     cropped_image = image[y_min:y_max, x_min:x_max]

#     # Преобразование обрезанного изображения в формат PIL и возврат результата
#     return Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))


# # Пример использования функции
# image_path = (
#     "/home/denis/DISK/MyProject/speakerpy/eyeeaseai/img_res/res_bg3_dx11_qs5wMkIhtj.jpg"
# )
# cropped_image = crop_text(image_path)
# cropped_image.show()
