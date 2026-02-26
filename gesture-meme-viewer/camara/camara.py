import cv2

class Camara:
    def __init__(self, indice=0):
        self.captura = cv2.VideoCapture(indice)

    def leer(self):
        return self.captura.read()

    def liberar(self):
        self.captura.release()