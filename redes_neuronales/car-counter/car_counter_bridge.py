import cv2
import numpy as np

# Cargar el video (reemplaza 'highway.mp4' con tu video)
cap = cv2.VideoCapture("CarsDrivingUnderBridge.mp4")

# Verificar si el video se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

# Obtener dimensiones del video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Crear el sustractor de fondo con configuración mejorada para sombras
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=500,  # Aumentado para mejor modelo de fondo
    varThreshold=50,  # Reducido para ser más sensible a cambios reales
    detectShadows=True,  # Mantener detección de sombras para poder filtrarlas
)

# Parámetros configurables mejorados
LINE_POSITION = frame_height // 2
MIN_CONTOUR_AREA = 800  # Aumentado para filtrar objetos pequeños (sombras)
MAX_CONTOUR_AREA = 15000  # Límite superior para evitar contornos demasiado grandes
CROSSING_TOLERANCE = 25
TRACKING_DISTANCE = 60  # Aumentado para mejor tracking
MIN_ASPECT_RATIO = 0.3  # Ratio mínimo ancho/alto para filtrar sombras alargadas
MAX_ASPECT_RATIO = 4.0  # Ratio máximo ancho/alto

vehicle_count = 0
tracked_objects = []
object_id = 0


def get_centroid(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return cx, cy
    return None


def is_valid_vehicle_contour(contour):
    """Filtrar contornos que probablemente sean vehículos y no sombras"""
    area = cv2.contourArea(contour)

    # Filtro por área
    if area < MIN_CONTOUR_AREA or area > MAX_CONTOUR_AREA:
        return False

    # Obtener rectángulo delimitador
    x, y, w, h = cv2.boundingRect(contour)

    # Filtro por aspect ratio (las sombras suelen ser muy alargadas)
    aspect_ratio = w / h if h > 0 else 0
    if aspect_ratio < MIN_ASPECT_RATIO or aspect_ratio > MAX_ASPECT_RATIO:
        return False

    # Filtro por densidad (ratio área del contorno vs área del rectángulo)
    rect_area = w * h
    density = area / rect_area if rect_area > 0 else 0
    if density < 0.3:  # Las sombras suelen tener baja densidad
        return False

    return True


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar el sustractor de fondo
    fgmask = fgbg.apply(frame)

    # Separar píxeles de sombra (valor 127) de píxeles de primer plano (valor 255)
    # Las sombras se detectan como valor 127 en MOG2
    shadow_mask = (fgmask == 127).astype(np.uint8) * 255
    foreground_mask = (fgmask == 255).astype(np.uint8) * 255

    # Aplicar operaciones morfológicas más agresivas para limpiar sombras
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    # Limpiar la máscara de primer plano
    foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel_small)
    foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel_large)
    foreground_mask = cv2.dilate(foreground_mask, kernel_small, iterations=1)

    # Aplicar filtro Gaussiano para suavizar
    foreground_mask = cv2.GaussianBlur(foreground_mask, (5, 5), 0)

    # Encontrar contornos en la máscara limpia
    contours, _ = cv2.findContours(
        foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    current_objects = []
    for contour in contours:
        if is_valid_vehicle_contour(contour):
            centroid = get_centroid(contour)
            if centroid:
                cx, cy = centroid
                current_objects.append((cx, cy))

                # Dibujar el contorno y el centroide
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                # Dibujar información del contorno para debug
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

    # Actualizar objetos rastreados con mejor lógica
    new_tracked_objects = []
    used_objects = set()

    # Primero, intentar emparejar objetos existentes
    for tid, tcx, tcy, counted in tracked_objects:
        best_match = None
        min_distance = TRACKING_DISTANCE

        for i, (cx, cy) in enumerate(current_objects):
            if i not in used_objects:
                distance = ((cx - tcx) ** 2 + (cy - tcy) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    best_match = i

        if best_match is not None:
            cx, cy = current_objects[best_match]
            new_tracked_objects.append((tid, cx, cy, counted))
            used_objects.add(best_match)

    # Agregar nuevos objetos no emparejados
    for i, (cx, cy) in enumerate(current_objects):
        if i not in used_objects:
            new_tracked_objects.append((object_id, cx, cy, False))
            object_id += 1

    # Contar vehículos que cruzan la línea
    for i, (tid, cx, cy, counted) in enumerate(new_tracked_objects):
        if (
            not counted
            and LINE_POSITION - CROSSING_TOLERANCE
            < cy
            < LINE_POSITION + CROSSING_TOLERANCE
        ):
            vehicle_count += 1
            new_tracked_objects[i] = (tid, cx, cy, True)
            # Dibujar el conteo en el frame
            cv2.putText(
                frame,
                f"ID {tid} counted",
                (cx, cy - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

    # Mantener solo objetos cerca de la línea de conteo (memoria limitada)
    tracked_objects = [
        (tid, cx, cy, counted)
        for tid, cx, cy, counted in new_tracked_objects
        if abs(cy - LINE_POSITION) < 150
    ]

    # Dibujar la línea de conteo
    cv2.line(frame, (0, LINE_POSITION), (frame_width, LINE_POSITION), (255, 0, 0), 3)
    cv2.putText(
        frame,
        "Linea de Conteo",
        (10, LINE_POSITION - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2,
    )

    # Mostrar el conteo en la pantalla
    cv2.putText(
        frame,
        f"Vehiculos: {vehicle_count}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 255),
        3,
    )

    # Mostrar información de debug
    cv2.putText(
        frame,
        f"Objetos detectados: {len(current_objects)}",
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        frame,
        f"Objetos rastreados: {len(tracked_objects)}",
        (10, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    # Mostrar frames
    cv2.imshow("Frame", frame)
    cv2.imshow("Foreground Mask", foreground_mask)
    cv2.imshow("Shadow Mask", shadow_mask)  # Para debug de sombras

    # Salir con la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Total de vehículos contados: {vehicle_count}")
