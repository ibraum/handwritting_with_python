import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Charger le modèle entraîné
model = load_model('D:/handwrittingDetectionModel.h5')

# Charger et préparer l'image
image = cv2.imread('trainning/alphabets/alphabets.png', cv2.IMREAD_GRAYSCALE)
image_resized = cv2.resize(image, (28, 28))
image_normalized = image_resized / 255.0


# Interpréter et afficher le résultat
alphabets = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

predicted_alphabet = ""
while(predicted_alphabet):
    image_reshaped = image_normalized.reshape(1, 28, 28, 1)

    # Faire la prédiction
    prediction = model.predict(image_reshaped)
    predicted_class = np.argmax(prediction, axis=1)
    predicted_alphabet = alphabets[v]
    print(f"L'alphabet prédit est : {predicted_alphabet}")
