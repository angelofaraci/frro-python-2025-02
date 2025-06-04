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
linea_inferior = 1000
linea_superior = 100
linea_división = 970
offset = 4  # margen de error para el cruce de línea

# Contadores para entradas y salidas
contador_entrante = 0
contador_saliente = 0
contador_entrante_abajo = 0
contador_entrante_arriba = 0
contador_saliente_abajo = 0
contador_saliente_arriba = 0

# Substractor de fondo para detectar movimiento
fgbg = cv2.createBackgroundSubtractorMOG2(10, 1000, True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesamiento
    fgmask = fgbg.apply(frame)
    dilated = cv2.dilate(fgmask, np.ones((3,3)), iterations=4)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (0, linea_inferior), (frame.shape[1], linea_inferior), (0,255,0), offset)
    cv2.line(frame, (0, linea_superior), (frame.shape[1], linea_superior), (0,0,255), offset)
    cv2.line(frame, (linea_división,0), (linea_división+30, frame.shape[1]), (255,0,0), offset)
    
  
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filtra objetos pequeños
            x, y, w, h = cv2.boundingRect(cnt)
            cx = int(x + w/2)
            cy = int(y + h/2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,255,255), -1)

            # Conteo de entradas por abajo
            if (linea_inferior - offset) < cy < (linea_inferior + offset) and cx > linea_división:
                contador_entrante_abajo +=1
                contador_entrante += 1
                print(f'Auto entrante abajo: {contador_entrante}')
            # Conteo de salidas por abajo
            if (linea_inferior - offset) < cy < (linea_inferior + offset) and cx < linea_división:
                counted_salida = True
                contador_saliente_abajo +=1
                contador_saliente += 1
                print(f'Auto entrante abajo: {contador_entrante}')
            # Conteo de entradas por arriba
            if (linea_superior - offset) < cy < (linea_superior + offset) and cx < linea_división:
                contador_entrante_arriba += 1
                contador_entrante += 1
                print(f'Auto saliendo: {contador_saliente}')
            
            if (linea_superior - offset) < cy < (linea_superior + offset) and cx > linea_división:
                contador_saliente_arriba += 1
                contador_saliente += 1
                print(f'Auto saliendo: {contador_saliente}')
 
    cv2.putText(frame, f'entradas: {contador_entrante}', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f'salidas: {contador_saliente}', (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(frame, f'entradas abajo: {contador_entrante_abajo}', (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f'salientes abajo: {contador_saliente_abajo}', (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(frame, f'entradas arriba: {contador_entrante_arriba}', (10,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f'salidas arriba: {contador_saliente_arriba}', (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('Dilated', dilated)
    cv2.imshow('Mascara de Fondo', fgmask)
    cv2.imshow('Contador de Autos', frame)
    
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()