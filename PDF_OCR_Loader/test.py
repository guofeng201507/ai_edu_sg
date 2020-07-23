import os
from ocr_loader_m import convert_pdf_to_image_to_text

current_dir = os.getcwd()
first_parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
second_parent_dir = os.path.abspath(os.path.join(current_dir, "../.."))

pdf_path = './AR/NASDAQ_AMZN_2019.pdf'

pass
convert_pdf_to_image_to_text(pdf_path)