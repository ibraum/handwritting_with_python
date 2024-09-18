import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def remove_noise(img):
    return cv2.medianBlur(img, 5)
    
    
def grayscale(img):
    return  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

def thresholding(img):
    _ , imgT = cv2.threshold(img,0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return imgT
    
    
def read_text(img):
    text = pytesseract.image_to_string(img, config="--psm 6")
    return text

# gui = tk.Tk()
#ouvrir une fenêtre pour choisir l'image
file_path = filedialog.askopenfilename(
    title="Choisissez une image",
    filetypes=[("Fichiers d'image", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
)

# img = 
# gui.mainloop()
# Lire l'image
img = cv2.imread(file_path)


if img is None:
    print("Erreur: Impossible de charger l'image. Vérifiez le chemin du fichier.")
else:
    # Appliquer les transformations
    img = grayscale(img)
    img = remove_noise(img)
    img = thresholding(img)

    # Lire le texte avec Tesseract
    text = read_text(img)
    