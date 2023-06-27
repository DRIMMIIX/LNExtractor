import os
import PyPDF2
import time 
import pdfminer
from pdfminer.high_level import extract_text
from natsort import natsorted
from endswiths import ends_with
import argparse



def split_pdf(input_path):
    pdf_reader = PyPDF2.PdfReader(input_path)

    folder_name = f'{input_path}_folder'
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass

    for page_number in range(len(pdf_reader.pages)):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_number])

        output_path = os.path.join(folder_name, f"page{page_number + 1}.pdf")

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"Page {page_number+1} saved as {output_path}")
    return folder_name,output_path



def get_text(folder_name):
    files = natsorted(os.listdir(folder_name))
    output_folder = os.path.join(folder_name, "extracted_pages")
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass
 
    for i, pdf_file in enumerate(files):
        
        time.sleep(0.5)

        file_path = os.path.join(folder_name, pdf_file)

        text = extract_text(file_path)
        
        



        output_txt_files = os.path.join(output_folder, f"page{i+1}.txt")
        with open(output_txt_files, "w",encoding="utf-8") as output_file:
            
            output_file.write(text)



        print("Text extraction done. Output file:", output_txt_files)





def rerange_text(folder_name,output_path,):
    if os.path.exists(output_path):
        print("Files found. Starting text re-arrangement...")
        
        output_folder = os.path.join(folder_name, "extracted_pages")
        anagram_folder = os.path.join(folder_name, "rearranged_text")
        try:
            os.mkdir(anagram_folder)
        except FileExistsError:
            os.mkdir(anagram_folder)
        
        files = natsorted(os.listdir(output_folder))
        
        #splitting the vertical text into horizontal parts
        for i, txt_file in enumerate(files):
            txt_path = os.path.join(output_folder, txt_file)
            characters = ""
            with open(txt_path, "r", encoding="utf-8") as file:
                for line in file:
                    
                    line = line.strip()
                    if line.endswith(str([end for end in ends_with])) or len(line) > 10:
                        characters += line + "\n"
                    elif line.startswith("（") and line.endswith("）") or line.startswith('【') and line.endswith('】'):
                        characters += line + "\n"
                        
                    else:
                        characters += line

            # Save the re-arranged text
            rearranged_path = os.path.join(anagram_folder, txt_file)
            with open(rearranged_path, "w", encoding="utf-8") as output_file:
                output_file.write(characters)

        print("Text re-arrangement done.")

        
        # Loop through the rearranged_text folder and split lines longer than 13 characters
        rearranged_folder = os.path.join(folder_name, "rearranged_text")
        rearranged_files = natsorted(os.listdir(rearranged_folder))

        for txt_file in rearranged_files:
            txt_path = os.path.join(rearranged_folder, txt_file)
            updated_lines = []
            with open(txt_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    #splitting when there is ?, or etc. but also when character is longer than 24
                    if len(line) > 24 and not line.endswith(("?", "。", ",", "!", "】", "、", "？")):
                        split_lines = [line[i:i+24] for i in range(0, len(line), 24)]
                        updated_lines.extend(split_lines)
                    else:
                        updated_lines.append(line)

            # Save the updated lines
            with open(txt_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(updated_lines))

        print("Line splitting done.")
    else:
        print("Files not found.")

import sys

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
            print('its an image')

    if '.pdf' in file:
        file = str(file)
        folder_name, output_path = split_pdf(file)
        get_text(folder_name)
        rerange_text(folder_name, output_path)


if __name__ == '__main__':

    main(input("Enter file path: "))

'''img = cv2.imread('src/img2.png')

# Convert the image to grayscale using OpenCV
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Perform OCR on the grayscale image using Tesseract
text = pytesseract.image_to_string(Image.fromarray(gray_img), lang='jpn_vert')

print(text.splitlines())
text_lines = text.splitlines()

pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

c = canvas.Canvas('text.pdf')
c.setFont('HeiseiMin-W3', 12)

# Add each line of text to the PDF
y = 750
for line in text_lines:
    c.drawString(100, y, line)
    y -= 20

c.showPage()  # Create a new page
c.save()  # Save the PDF file
'''
