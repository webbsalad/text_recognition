import os
import csv
from PIL import Image

# Функция для определения нового значения пикселя на основе его текущего значения и соседних пикселей
def get_pixel_value(pixel, neighbors):
    # Подсчитываем количество черных соседей (значение 0)
    black_neighbors = sum(1 for neighbor in neighbors if neighbor == 0)
    
    # Возвращаем новое значение пикселя на основе различных условий
    if pixel == 0:
        return 1
    elif black_neighbors >= 2:
        return 0.75
    elif black_neighbors == 1:
        return 0.5
    elif 0 in neighbors:
        return 0.25
    elif 0.15 in neighbors:
        return 0.15
    elif 0.1 in neighbors:
        return 0.1
    else:
        return 0

# Функция для обновления массива значениями пикселей из изображения
def update_array_with_image(array, image_path):
    img = Image.open(image_path)  # Открываем файл изображения
    
    square_size = 32  # Размер квадрата
    width, height = img.size  # Получаем размеры изображения
    num_squares = 0  # Счетчик квадратов
    
    # Проходим по изображению квадратами размером 32x32 пикселя
    for x in range(0, width, square_size):
        for y in range(0, height, square_size):
            box = (x, y, x + square_size, y + square_size)
            square = img.crop(box)  # Вырезаем квадрат из изображения
            square = square.convert('L')  # Конвертируем изображение в градации серого
            pixel_data = list(square.getdata())  # Получаем данные пикселей
            
            # Проходим по данным пикселей и рассчитываем новые значения на основе соседей
            for i in range(len(pixel_data)):
                neighbors = []
                if i - 1 >= 0:
                    neighbors.append(pixel_data[i - 1])
                if i + 1 < len(pixel_data):
                    neighbors.append(pixel_data[i + 1])
                if i - square_size >= 0:
                    neighbors.append(pixel_data[i - square_size])
                if i + square_size < len(pixel_data):
                    neighbors.append(pixel_data[i + square_size])
                
                # Получаем новое значение пикселя
                new_value = get_pixel_value(pixel_data[i], neighbors)
                array[i] += new_value  # Обновляем массив новыми значениями
            
            num_squares += 1
    
    # Нормализуем значения в массиве, деля их на количество квадратов
    array = [element / num_squares for element in array]
    
    return array

# Функция для преобразования изображений в папке в массив
def image_folder_to_array(folder_path):
    array = [0] * 1024  # Инициализируем массив нулями
    
    # Считаем количество изображений в папке
    num_images = len([name for name in os.listdir(folder_path) if name.endswith('.png')])
    
    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)  # Полный путь к изображению
            array = update_array_with_image(array, image_path)  # Обновляем массив значениями из изображения
    
    # Нормализуем значения в массиве, деля их на количество изображений
    array = [element / num_images for element in array]
    
    return array

# Основная функция
def main():
    root_folder = "D:/text_det/letters"  # Корневая папка с изображениями
    result_file = "res.csv"  # Имя файла для записи результатов
    
    # Открываем CSV файл для записи
    with open(result_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Записываем первую строку с эталонными значениями
        for char in [0, 0.25, 0.5, 0.75, 1]:
            csvwriter.writerow(['.'] + [char] * 1024)
        
        # Проходим по всем файлам в корневой папке
        for filename in os.listdir(root_folder):
            if filename.endswith('.png'):
                image_path = os.path.join(root_folder, filename)  # Полный путь к изображению
                result_array = update_array_with_image([0] * 1024, image_path)  # Обновляем массив
                csvwriter.writerow([filename[:-4]] + result_array)  # Записываем результат в CSV
    
    print("Готово")

# Запускаем основную функцию
if __name__ == "__main__":
    main()
