import pytesseract
import cv2

# Configuración de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = cv2.imread('img_test.jpg')
text = pytesseract.image_to_string(image, lang='spa')
print(text)

cv2.imshow('Imagen de prueba', image)
cv2.waitKey(0)
cv2.destroyAllWindows()