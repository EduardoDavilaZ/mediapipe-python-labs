import math

def punio(landmarks):
    return (
        landmarks[8].y > landmarks[6].y and #indice OFF
        landmarks[12].y > landmarks[10].y and #medio OFF
        landmarks[16].y > landmarks[14].y and #anular OFF
        landmarks[20].y > landmarks[18].y #meñique OFF
    )

def mano_abierta(landmarks):
    return (
        landmarks[8].y < landmarks[6].y and #indice ON
        landmarks[12].y < landmarks[10].y and #medio ON
        landmarks[16].y < landmarks[14].y 
    )

def victoria(landmarks):
    return (
        landmarks[8].y < landmarks[6].y and #indice ON
        landmarks[12].y < landmarks[10].y and #medio ON
        landmarks[16].y > landmarks[14].y and #anular OFF
        landmarks[20].y > landmarks[18].y #meñique OFF
    )

# def fuck(landmarks):
#     return (
#         landmarks[8].y > landmarks[6].y and #indice OFF
#         landmarks[12].y < landmarks[10].y and #medio ON

#         landmarks[16].y > landmarks[14].y and #anular OFF
#         landmarks[20].y > landmarks[18].y #meñique OFF
#     )

def corazon(landmarks):
    return (
        landmarks[8].y < landmarks[6].y and
        landmarks[4].y < landmarks[1].y and
        0.03 > math.sqrt((landmarks[3].x - landmarks[7].x)**2 + (landmarks[3].y - landmarks[7].y)**2)
    )

def ok(landmarks):
    return (
        landmarks[12].y < landmarks[10].y and #medio ON
        landmarks[16].y < landmarks[14].y and #anular ON
        landmarks[20].y < landmarks[18].y and #meñique ON
        0.05 > math.sqrt((landmarks[8].x - landmarks[4].x)**2 + (landmarks[8].y - landmarks[4].y)**2)
    )
