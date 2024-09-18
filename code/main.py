import cv2
import pytesseract
import pandas as pd
# import easyocr
# from easyocr import Reader
# import torch

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread(r'trainning/dos/new.jpg')
#obtenir les dimensions de l'image
# img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_LINEAR)
(height, width) = img.shape[:2]

print(height, width)
x = 0
y = 0
half_width = int( width / 2)
print(height, half_width)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
left = gray[y:height, x:half_width]
right = gray[y:height, half_width:width]



# reader = easyocr.Reader(['fr'])

ret, thresh1 = cv2.threshold(right, 120, 255, cv2.THRESH_BINARY)

cv2.imshow("tresh1", thresh1)
cv2.imshow("img_right", right)
cv2.waitKey(0)
cv2.destroyAllWindows
# result = reader.readtext(right)

# print(result)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

im2 = right.copy()

# # Initialiser EasyOCR
# # reader = easyocr.Reader(['en', 'fr'])  # Vous pouvez ajouter d'autres langues si nécessaire
# text_positions = []

questions = []
answers = []

for cnt in contours:

    x, y, w, h = cv2.boundingRect(cnt)

    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    aspect_ratio = w / float(h)
    
    # Vérifier si le contour correspond à une case à cocher (carré)
    if 0.9 <= aspect_ratio <= 1.1 and 10 <= w <= 50:
        # Extraire la région de la case
        roi = thresh1[y:y + h, x:x + w]
        
        # Déterminer si la case est cochée
        non_zero_pixels = cv2.countNonZero(roi)
        total_pixels = roi.size
        answer = "Oui" if non_zero_pixels / total_pixels > 0.3 else ""
        
        # Identifier la question correspondante en extrayant du texte à proximité
        question_region = right[y - 30:y + h + 30, 0:x]  # Extraction du texte à gauche de la case
        question_text = pytesseract.image_to_string(question_region, config='--psm 6', lang='fra').strip()
        
        # Ajouter la question et la réponse aux listes
        questions.append(question_text)
        answers.append(answer)
    text = pytesseract.image_to_string(im2, config="--psm 6",  lang='fra')
    
    
df = pd.DataFrame({
    "Questions": questions,
    "Réponses": answers
})

# Sauvegarder les questions et réponses dans un fichier Excel
df.to_excel('recognition.xlsx', index=False)

print("Le fichier Excel 'output.xlsx' a été généré avec succès.")

#     # Nettoyer le texte pour ignorer les cases à cocher
#     cleaned_text = ''.join([c for c in text if c.isalpha() or c.isspace()])

#     if cleaned_text.strip():  # Si le texte n'est pas vide après nettoyage
#         text_positions.append((y, cleaned_text.strip()))

#     # Trier les textes par leur position verticale
#     text_positions.sort(key=lambda x: x[0])
    
#     # Reconnaître le texte dans la région d'intérêt avec EasyOCR
#     # result = reader.readtext(cropped)

#     # Extraire le texte reconnu
#     # for (bbox, text, prob) in result:
#     #     print("bbox : " + str(bbox) + "\ntext : " + str(text) + "\nprob : " + str(prob))
#     #     with open("eazyocr.txt", "a") as file:
#     #         file.write(text + "\n")
    
    
with open("recognized.txt", "a", encoding="utf-8") as file:
    # for text in text_positions:
        print(str(text))
        file.write(text)
        file.write("\n")
        file.close()