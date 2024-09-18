import cv2
import pytesseract
import pandas as pd
from openpyxl import Workbook

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Charger l'image
image = cv2.imread(r'E:\PROJECT\learning-python\handwrittingdetect\trainning\dos\new.jpg')
(height, width) = image.shape[:2]
print(height / 2, width / 2)
image = cv2.resize(image, (int(width / 2), int(height / 2)), interpolation=cv2.INTER_LINEAR)
(height, width) = image.shape[:2]

print(height, width)
x = 0
y = 0
half_width = int( width / 2)
print(height, half_width)
left = image[y:height, x:half_width]
right = image[y:height, half_width:width]



# Convertir l'image en niveaux de gris
gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

# Appliquer un seuil pour convertir l'image en binaire
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Trouver les contours des éléments de l'image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Liste pour stocker les questions et réponses
questions = []
answers = []

# Parcourir les contours pour détecter les cases à cocher
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = w / float(h)
    
    # Vérifier si le contour correspond à une case à cocher (carré)
    if 0.9 <= aspect_ratio <= 1.1 and 10 <= w <= 50:
        # Extraire la région de la case
        roi = binary[y:y + h, x:x + w]
        
        # Déterminer si la case est cochée
        non_zero_pixels = cv2.countNonZero(roi)
        total_pixels = roi.size
        answer = "Oui" if non_zero_pixels / total_pixels > 0.3 else "Non"
        
        # Identifier la question correspondante en extrayant du texte à proximité
        question_region = gray[y - 30:y + h + 30, 0:x]  # Extraction du texte à gauche de la case
        question_text = pytesseract.image_to_string(question_region, config='--psm 6', lang='eng').strip()
        
        # Ajouter la question et la réponse aux listes
        questions.append(question_text)
        answers.append(answer)

# Création du DataFrame Pandas pour les questions et les réponses
df = pd.DataFrame({
    "Questions": questions,
    "Réponses": answers
})

# Sauvegarder les questions et réponses dans un fichier Excel
df.to_excel('output_face.xlsx', index=False)

print("Le fichier Excel 'output.xlsx' a été généré avec succès.")
