import cv2
def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames

def detect_vehicles(frame):
    # Placeholder for vehicle detection logic
    # This function should implement a vehicle detection algorithm
    # such as using Haar cascades or a pre-trained deep learning model.
    pass

def draw_vehicle_count(frame, count):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'Count: {count}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)