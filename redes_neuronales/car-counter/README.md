# Car Counter Project

This project is designed to count cars entering and exiting a frame from a video using OpenCV. The video file used for this project is located in the `videos` folder and is named "Carretera".

## Project Structure

```
car-counter
├── src
│   ├── car_counter.py   # Main logic for counting cars
│   └── utils.py         # Utility functions for video processing
├── videos
│   └── Carretera        # Video file for counting cars
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd car-counter
   ```

2. **Install dependencies**:
   It is recommended to create a virtual environment before installing the dependencies. You can use `venv` or `conda` for this purpose.

   Using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Video File**:
   Ensure that the video file "Carretera" is placed in the `videos` folder.

## Usage

To run the car counting program, execute the following command:

```
python src/car_counter.py
```

This will start processing the video and display the count of cars entering and exiting the frame.

## Additional Information

- The project utilizes OpenCV for video processing and vehicle detection.
- Utility functions in `utils.py` assist with frame extraction and detection algorithms.
- Make sure to have the necessary permissions to access the video file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.