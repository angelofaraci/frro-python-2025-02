import cv2
import mediapipe as mp
import time
import os
from datetime import datetime

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Configuración para grabar video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30
video_writer = None
recording = False
countdown = 0
countdown_start = 0
action = None
last_action_time = 0
cooldown = 2  # Segundos de enfriamiento entre acciones

# Carpeta para guardar fotos y videos
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    # Convertir la imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Estado actual
    current_time = time.time()
    hand_detected = None

    # Procesar detección de manos
    if results.multi_hand_landmarks and not countdown and not recording:
        for hand_landmarks, hand_info in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            # Dibujar puntos clave de las manos
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determinar si es mano izquierda o derecha
            label = hand_info.classification[0].label  # 'Left' o 'Right'
            if label == "Left" and current_time - last_action_time > cooldown:
                hand_detected = "left"
            elif label == "Right" and current_time - last_action_time > cooldown:
                hand_detected = "right"

    # Iniciar conteo regresivo
    if hand_detected and not countdown and not recording:
        countdown = 5  # 5 segundos de conteo regresivo
        countdown_start = current_time
        action = hand_detected

    # Mostrar conteo regresivo
    if countdown > 0:
        elapsed = current_time - countdown_start
        remaining = max(0, countdown - int(elapsed))
        cv2.putText(
            frame,
            f"Conteo: {remaining}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        if remaining == 0:
            countdown = 0
            last_action_time = current_time

            if action == "left":
                # Tomar foto
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                photo_path = os.path.join(output_dir, f"photo_{timestamp}.png")
                cv2.imwrite(photo_path, frame)
                print(f"Foto guardada en: {photo_path}")

            elif action == "right":
                # Iniciar grabación de video
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = os.path.join(output_dir, f"video_{timestamp}.mp4")
                video_writer = cv2.VideoWriter(
                    video_path,
                    cv2.VideoWriter_fourcc(*"mp4v"),
                    fps,
                    (frame_width, frame_height),
                )
                recording = True
                print(f"Grabando video: {video_path}")

    # Grabar video si está activo
    if recording:
        video_writer.write(frame)
        cv2.putText(
            frame, "Grabando...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )
        # Detener grabación después de 5 segundos
        if current_time - last_action_time > 5:
            recording = False
            video_writer.release()
            video_writer = None
            print("Grabación finalizada.")

    # Mostrar el frame
    cv2.imshow("Hand Action Camera", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
if video_writer is not None:
    video_writer.release()
cv2.destroyAllWindows()
hands.close()
