import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Charger le modèle entraîné
model = load_model('D:/handwrittingDetectionModel.h5')

# Charger et préparer l'image
image = cv2.imread('a.png', cv2.IMREAD_GRAYSCALE)
height, width = image.shape

# Définir la taille de la fenêtre
window_size = 28

# Initialiser la chaîne de texte prédit
predicted_text = ""
alphabets = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Glisser une fenêtre de 28x28 pixels sur la largeur de l'image
for i in range(0, width - window_size + 1, window_size):
    # Extraire la sous-image (fenêtre) actuelle
    image_segment = image[0:height, i:i + window_size]

    # Redimensionner la sous-image à 28x28 pixels (au cas où la hauteur est différente)
    image_resized = cv2.resize(image_segment, (window_size, window_size))

    # Normaliser l'image
    image_normalized = image_resized / 255.0

    # Reshaper l'image pour correspondre à l'entrée du modèle
    image_reshaped = image_normalized.reshape(1, 28, 28, 1)

    # Faire la prédiction
    prediction = model.predict(image_reshaped)
    predicted_class = np.argmax(prediction, axis=1)
    predicted_alphabet = alphabets[predicted_class[0]]

    # Ajouter le résultat prédit à la chaîne de texte
    predicted_text += predicted_alphabet

# Afficher la phrase prédite
print(f"La phrase prédite est : {predicted_text}")
