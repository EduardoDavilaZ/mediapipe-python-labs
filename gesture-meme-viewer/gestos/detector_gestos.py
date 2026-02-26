from gestos.gestos import punio, mano_abierta, victoria, corazon, ok

class DetectorGestos:
    def detectar(self, landmarks):
        if corazon(landmarks):
            return "corazón coreano"
        if ok(landmarks):
            return "oks"
        # if fuck(landmarks):
        #     return "Eso no bro"
        if punio(landmarks):
            return "Puño"
        if victoria(landmarks):
            return "Kawaiii"
        if mano_abierta(landmarks):
            return "Mano abierta"
        return "NULL"
