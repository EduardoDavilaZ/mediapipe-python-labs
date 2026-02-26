import cv2
from camara.camara import Camara
from seguimiento_mano.detector_mano import DetectorMano
from gestos.detector_gestos import DetectorGestos

camara = Camara()
detector_mano = DetectorMano()
detector_gestos = DetectorGestos()

while True:
    ret, frame = camara.leer()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    resultado = detector_mano.procesar(frame)

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            detector_mano.dibujar(frame, mano)
            gesto = detector_gestos.detectar(mano.landmark)
            print(gesto)

    cv2.imshow("Gestos de la Mano", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.liberar()
cv2.destroyAllWindows()
