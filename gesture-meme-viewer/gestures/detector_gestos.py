from gestos.gestos import punio, mano_abierta, victoria, corazon, ok

class DetectorGestos:
    def detectar(self, landmarks):
        if corazon(landmarks):
            return "corazon.jpg"
        if ok(landmarks):
            return "ok.jpg"
        # if fuck(landmarks):
        #     return "Eso no bro"
        if punio(landmarks):
            return "punio.jpg"
        if victoria(landmarks):
            return "kawaii.jpg"
        if mano_abierta(landmarks):
            return "mano_abierta.gif"
        return "none.jpg"
