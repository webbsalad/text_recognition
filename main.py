import csv
from PIL import Image
import os

# Функция для обновления массива значениями пикселей из изображения
def update_array_with_image(array, image_path):
    img = Image.open(image_path)  # Открываем изображение
    img = img.convert('L')  # Конвертируем изображение в градации серого
    pixel_data = list(img.getdata())  # Получаем данные пикселей
    updated_array = [array[i] + (1 if pixel == 0 else 0) for i, pixel in enumerate(pixel_data)]  # Обновляем массив
    return updated_array

# Функция для преобразования изображения в массивы субизображений
def image_to_array(image_path):
    subimages_array = []  # Список для хранения массивов субизображений
    img = Image.open(image_path)  # Открываем изображение
    img = img.convert('L')  # Конвертируем изображение в градации серого
    width, height = img.size  # Получаем размеры изображения
    
    # Подсчитываем количество горизонтальных и вертикальных субизображений
    horizontal_subimages = width // 32
    vertical_subimages = height // 32

    # Проходим по изображению, выделяя квадраты размером 32x32 пикселя
    for y in range(0, height, 32):
        for x in range(0, width, 32):
            subimage = img.crop((x, y, x+32, y+32))  # Вырезаем субизображение
            pixel_data = list(subimage.getdata())  # Получаем данные пикселей субизображения
            black_pixel_count = sum(1 for pixel in pixel_data if pixel == 0)  # Считаем черные пиксели
            if black_pixel_count / 1024 >= 0.1:  # Если доля черных пикселей >= 10%
                array = [0] * 1024  # Инициализируем массив нулями
                array = [array[i] + (1 if pixel == 0 else 0) for i, pixel in enumerate(pixel_data)]  # Обновляем массив
                subimages_array.append(array)  # Добавляем массив в список
            else:
                subimages_array.append(None)  # Добавляем None, если субизображение не подходит
    return subimages_array

# Функция для вычисления квадратного корня методом Ньютона
def sqrt(x):
    guess = x
    epsilon = 0.000001  # Точность вычисления
    while abs(guess * guess - x) > epsilon:
        guess = (guess + x / guess) / 2
    return guess

# Функция для расчета расстояния между двумя массивами
def calculate_distance(array1, array2):
    squared_diff_sum = 0
    for i in range(len(array1)):
        squared_diff_sum += (array1[i] - array2[i]) ** 2
    return sqrt(squared_diff_sum)

# Функция для поиска самого похожего изображения
def find_most_similar_image(input_array, images):
    min_distance = float('inf')
    most_similar_image = None
    
    for image_name, image_array in images.items():
        distance = calculate_distance(input_array, image_array)  # Расчет расстояния до текущего изображения
        if distance < min_distance:
            min_distance = distance
            most_similar_image = image_name  # Обновляем наиболее похожее изображение
    
    return most_similar_image

# Основная функция
def main():
    reference_file_path = "res.csv"  # Путь к CSV файлу с эталонными изображениями
    image_path = "test.png"  # Путь к изображению студента

    subimages_array = image_to_array(image_path)  # Преобразуем изображение в массивы субизображений

    images = {}  # Словарь для хранения эталонных изображений
    with open(reference_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            images[row[0]] = list(map(float, row[1:]))  # Считываем данные из CSV файла

    result_text = ""
    for subimage_array in subimages_array:
        if subimage_array is not None:
            most_similar_image = find_most_similar_image(subimage_array, images)  # Поиск наиболее похожего изображения
            result_text += most_similar_image  # Добавляем имя изображения к результату
        else:
            result_text += " "  # Добавляем пробел, если субизображение не подходит

    print("==", result_text)

# Запускаем основную функцию
if __name__ == "__main__":
    main()
