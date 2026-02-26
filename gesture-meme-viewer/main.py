import cv2
import imageio
from camera.camara import Camara
from hand_tracking.detector_mano import DetectorMano
from gestures.detector_gestos import DetectorGestos
import config

# ===========
# INICIALIZAR
# ===========
camara = Camara(ancho=config.FRAME_WIDTH, alto=config.FRAME_HEIGHT)
detector_mano = DetectorMano()
detector_gestos = DetectorGestos()

gesto_actual = config.MEME_DEFAULT
frames_gif = []
frame_index = 0
imagen_estatica = None


# Función que carga la imágen o gif
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def cargar_recurso(nombre_archivo):
    global frames_gif, imagen_estatica, frame_index
    frames_gif = []
    imagen_estatica = None
    frame_index = 0

    ruta = config.ASSETS_DIR + "/" + nombre_archivo

    if not cv2.os.path.exists(ruta):
        return

    if nombre_archivo.lower().endswith(".gif"):
        gif_frames = imageio.mimread(ruta)
        frames_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif_frames]
    else:
        imagen = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)
        if imagen is not None:
            # Redimensionamos al tamaño fijo del meme
            imagen_estatica = cv2.resize(imagen, (config.MEME_WIDTH, config.MEME_HEIGHT))


cargar_recurso(gesto_actual) # Cargar meme por defecto



# ==========
# VENTANAS
# ==========
cv2.namedWindow("Gestos de la Mano", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Gestos de la Mano", config.FRAME_WIDTH, config.FRAME_HEIGHT)

cv2.namedWindow("Meme", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Meme", config.MEME_WIDTH, config.MEME_HEIGHT)



# ================
# BUCLE PRINCIPAL
# ================
while True:
    ret, frame = camara.leer()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    resultado = detector_mano.procesar(frame)

    nuevo_gesto = config.MEME_DEFAULT  # por defecto siempre none


    # Detección de gestos con landmarks
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            detector_mano.dibujar(frame, mano)
            detectado = detector_gestos.detectar(mano.landmark)
            if detectado:
                nuevo_gesto = detectado


    # Si cambia el gesto, cambia el recurso
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if nuevo_gesto != gesto_actual:
        gesto_actual = nuevo_gesto
        cargar_recurso(gesto_actual)

    
    # Aquí se muestra la imágen (meme)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    if frames_gif:
        meme_frame = frames_gif[frame_index]
        frame_index = (frame_index + 1) % len(frames_gif)
        meme_frame = cv2.resize(meme_frame, (config.MEME_WIDTH, config.MEME_HEIGHT))
        cv2.imshow("Meme", meme_frame)
    elif imagen_estatica is not None:
        cv2.imshow("Meme", imagen_estatica)



    # Mostrar cámara
    # ^^^^^^^^^^^^^^^
    cv2.imshow("Gestos de la Mano", frame)

    if cv2.waitKey(30) == ord('q'): # Salir con 'q'
        break

# Limpieza
# ^^^^^^^^
camara.liberar()
cv2.destroyAllWindows()