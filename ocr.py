import cv2
import pytesseract as pyt
import multiprocessing

def ocr():
    # Charger l'image
    image = cv2.imread('exemple5.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialiser le détecteur MSER
    mser = cv2.MSER_create()

    # Détecter les régions MSER dans l'image
    regions, _ = mser.detectRegions(gray)

    # Créer une copie de l'image pour afficher les régions détectées
    output = image.copy()

    # Dessiner les contours des régions détectées
    text = []
    for region in regions:
        hull = cv2.convexHull(region.reshape(-1, 1, 2))
        cv2.polylines(output, [hull], True, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(hull)
        roi = gray[y:y + h, x:x + w]
        text = pyt.image_to_string(roi, config="utf-8")
        # print(text)
        f = open("regions.txt", 'a')
        f.write(str(text))
        f.write("\n")
        f.write("\n")
        # text.append()

    # Afficher l'image avec les régions détectées
    cv2.imshow('Text Regions', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    p = multiprocessing.Process(target=ocr, args=())
    p.start()
    p.join()