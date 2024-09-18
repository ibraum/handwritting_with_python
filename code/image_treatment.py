import cv2
import os
import numpy as np
from tensorflow.keras.utils import to_categorical

# Chemin vers les répertoires d'images
data_dir = 'trainning'
categories = ['face', 'dos']  # Liste des catégories
img_size = 150

def load_images(data_dir, categories, img_size):
    data = []
    labels = []
    for category in categories:
        path = os.path.join(data_dir, category)
        print("Le chamin est " + str(path))
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                resized_array = cv2.resize(img_array, (img_size, img_size * 2))
                data.append(resized_array)
                labels.append(class_num)
            except Exception as e:
                pass
    return np.array(data), np.array(labels)

data, labels = load_images(data_dir, categories, img_size)
data = data / 255.0  # Normalisation des images
print(data)
labels = to_categorical(labels, num_classes=len(categories))
print(labels)