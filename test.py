import csv
import numpy as np
from PIL import Image

def create_image(grid_size, symbol_data, output_path):

    image = Image.new('L', (grid_size[0] * 32, grid_size[1] * 32), color=255)

    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            symbol_index = y * grid_size[0] + x
            if symbol_index < len(symbol_data):
                symbol_values = list(map(float, symbol_data[symbol_index]))  
                symbol_array = np.array(symbol_values).reshape((32, 32)) * 255  
                symbol_image = Image.fromarray(symbol_array.astype(np.uint8))
                image.paste(symbol_image, (x * 32, y * 32))
    
    image.save(output_path)

def main():

    grid_size = (8, 8)
    
    res_csv_path = "res.csv"
    
    symbol_data = []
    with open(res_csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            symbol_values = row[1:]
            symbol_data.append(symbol_values)
    
    output_path = "grid.png"
    create_image(grid_size, symbol_data, output_path)
    print("Done")

if __name__ == "__main__":
    main()
