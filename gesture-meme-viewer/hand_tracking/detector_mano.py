import cv2
import mediapipe as mp

class DetectorMano:
    def __init__(self):
        self.mp_manos = mp.solutions.hands
        self.manos = self.mp_manos.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.dibujador = mp.solutions.drawing_utils

    def procesar(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.manos.process(rgb)

    def dibujar(self, frame, landmarks_mano):
        self.dibujador.draw_landmarks(
            frame,
            landmarks_mano,
            self.mp_manos.HAND_CONNECTIONS
        )
