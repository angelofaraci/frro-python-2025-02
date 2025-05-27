import cv2

class CarCounter:
    def __init__(self, video_path):
        self.video_path = video_path
        self.car_count = 0
        self.exit_count = 0
        self.tracker = cv2.TrackerKCF_create()
        self.init_tracker = False

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if not self.init_tracker:
                self.initialize_tracker(frame)
                self.init_tracker = True

            success, bbox = self.tracker.update(frame)
            if success:
                self.update_counts(bbox)

            self.display_frame(frame)

        cap.release()
        cv2.destroyAllWindows()

    def initialize_tracker(self, frame):
        # Initialize the tracker with the first frame and bounding box
        bbox = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        self.tracker.init(frame, bbox)

    def update_counts(self, bbox):
        # Update car counts based on bounding box position
        x, y, w, h = [int(v) for v in bbox]
        if y < 200:  # Assuming the upper limit for entering cars
            self.car_count += 1
        elif y > 400:  # Assuming the lower limit for exiting cars
            self.exit_count += 1

    def display_frame(self, frame):
        cv2.putText(frame, f'Cars Entered: {self.car_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Cars Exited: {self.exit_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

if __name__ == "__main__":
    video_path = '../videos/Carretera'  # Update with the correct video file path
    car_counter = CarCounter(video_path)
    car_counter.process_video()