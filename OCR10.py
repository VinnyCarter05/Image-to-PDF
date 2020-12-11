import cv2, os
import pytesseract
import numpy as np
from pdf2image import convert_from_path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
''' need to install pdf2image and Poppler and add Poppler\bin to path'''

filepath = "Faxes\zivkovic, stana.pdf"

def convertToImgs(path, imgtype=".tif"):
    pages=convert_from_path(path)
    newPath, _ = os.path.splitext(path)
    for i in range(len(pages)):
        pages[i].save(f"{newPath}({i}){imgtype}")
convertToImgs(filepath)

img = cv2.imread("Faxes\zivkovic, stana(2).tif")
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# gray = cv2.bitwise_not(img_bin)
kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(img, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)