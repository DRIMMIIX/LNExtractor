from pdf_extracting import *
from image_extraction import *

image_types = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
    ".svg",
    ".raw",
    ".psd",
    ".ai",
    ".eps",
    
]


def main(file):
    print(type(file))

    for img_type in image_types:
        if img_type in file:
            extract_text(file)

    if '.pdf' in file:
        file = str(file)
        folder_name, output_path = split_pdf(file)
        get_text(folder_name)
        rerange_text(folder_name, output_path)


if __name__ == '__main__':

    main(input("Enter file path: "))