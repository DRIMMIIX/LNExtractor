import pytesseract
from PIL import Image
import cv2
import os

import cv2
import numpy as np

def prepare_image(image_path):
    # Load the image in color
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(threshold, kernel, iterations=2)

    return dilated




def extract_text(image_folder):
    #for a folder
    if os.path.isdir(image_folder):
        print("The path is a directory/folder.")

        output_folder = 'output_' + str(image_folder)
        os.makedirs(output_folder, exist_ok=True)
        #creates a folder with individual extratced txt files from the image source
        for file_name in os.listdir(image_folder):
            file_path = os.path.join(image_folder, file_name)
            if os.path.isfile(file_path):
                preprocessed_image = prepare_image(file_path)
                custom_config = r"--oem 3 --psm 6 -l jpn_vert"
                extracted_text =  pytesseract.image_to_string(Image.fromarray(preprocessed_image), lang='jpn_vert')
                output_file_path = os.path.join(output_folder, f"output_{file_name}.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_text:
                    output_text.write(extracted_text.replace('\uFFFD', '<?>'))
                print(f"Processed file: {file_name}")
    else:
        #creates a folder with individual extratced txt files from the image source
        #extra mde for one file
        output_folder = 'output_' + str(image_folder)
        os.makedirs(output_folder, exist_ok=True)
        if os.path.isfile(image_folder):
            preprocessed_image = prepare_image(image_folder)
            custom_config = r"--oem 3 --psm 6 -l jpn_vert"
            extracted_text = pytesseract.image_to_string(Image.fromarray(preprocessed_image), lang='jpn_vert')
            output_file_path = os.path.join(output_folder, f"output_{os.path.basename(image_folder)}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as output_text:
                output_text.write(extracted_text.replace('\uFFFD', '<?>'))
            print(f"Processed file: {os.path.basename(image_folder)}")

