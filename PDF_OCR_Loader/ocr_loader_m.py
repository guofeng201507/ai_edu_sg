# Import libraries
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

# https://www.testpapersfree.com/

def convert_pdf_to_image_to_text(file_path):
    '''
    Part #1 : Converting PDF to images
    '''

    filename = file_path.split('/')[-1][: -4]
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(file_path, 500)
    # Counter to store images of each page of PDF to image
    image_folder = './' + filename + '/'
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)
    image_counter = 1
    # Iterate through all the pages stored above
    for page in pages:
        filename = "page_" + str(image_counter) + ".jpg"
        page.save(image_folder + filename, 'JPEG')
        image_counter = image_counter + 1

        '''
    Part #2 - Recognizing text from the images using OCR
    '''
    filelimit = image_counter - 1
    outfile = image_folder + "out_text.txt"

    f = open(outfile, "a", encoding='utf-8')
    for i in range(1, filelimit + 1):
        # for i in [3, 5, 6, 7, 8]:
        filename = "page_" + str(i) + ".jpg"
        text = str(((pytesseract.image_to_string(Image.open(image_folder + filename)))))

        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')
        f.write(text)

    f.close()

    return image_counter

