import cv2
import pytesseract
import numpy as np
import pandas as pd

# Charger l'image
image = cv2.imread('trainning/dos/new.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Détecter les contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

data = {}
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 50 and h > 20:  # Exclure les petits bruits
        roi = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
        # Déterminer si c'est une case à cocher
        if h < 50 and w < 50:  # Condition simple pour une case à cocher
            checked = np.mean(roi) < 200  # Analyse simple
            data[f'Case at ({x}, {y})'] = 'Cochée' if checked else 'Non cochée'
        else:
            data[f'Text at ({x}, {y})'] = text.strip()

# Exporter vers Excel
df = pd.DataFrame([data])
df.to_excel('output.xlsx', index=False)
