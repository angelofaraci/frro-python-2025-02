import cv2
import numpy as np

# Ruta al video

cap = cv2.VideoCapture("redes_neuronales/car-counter/carretera_video.mp4")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
if not cap.isOpened():
    print("Error al abrir el video.")
    exit()
# Línea virtual para contar autos (ajusta según el video)
linea_entrada = 1000
linea_salida = 100
offset = 7  # margen de error para el cruce de línea

contador_entrada = 0
contador_salida = 0

# Substractor de fondo para detectar movimiento
fgbg = cv2.createBackgroundSubtractorMOG2(10, 600, False)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesamiento
    fgmask = fgbg.apply(frame)
    dilated = cv2.dilate(fgmask, np.ones((6,6)), iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (0, linea_entrada), (frame.shape[1], linea_entrada), (0,255,0), offset)
    cv2.line(frame, (0, linea_salida), (frame.shape[1], linea_salida), (0,0,255), offset)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filtra objetos pequeños
            x, y, w, h = cv2.boundingRect(cnt)
            cx = int(x + w/2)
            cy = int(y + h/2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,255,255), -1)

            # Conteo de entrada
            if (linea_entrada - offset) < cy < (linea_entrada + offset):
                contador_entrada += 1
                print(f'Auto entrante: {contador_entrada}')
            # Conteo de salida
            if (linea_salida - offset) < cy < (linea_salida + offset):
                contador_salida += 1
                print(f'Auto saliendo: {contador_salida}')

    cv2.putText(frame, f'Entradas: {contador_entrada}', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f'Salidas: {contador_salida}', (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('Contador de Autos', frame)
    cv2.imshow('Mascara de Fondo', fgmask)
    cv2.imshow('Dilated', dilated)
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()