import cv2

class Camara:
    def __init__(self, indice=0, ancho=640, alto=480):
        self.captura = cv2.VideoCapture(indice)

        # 🔥 Forzar resolución
        self.captura.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self.captura.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

    def leer(self):
        return self.captura.read()

    def liberar(self):
        self.captura.release()