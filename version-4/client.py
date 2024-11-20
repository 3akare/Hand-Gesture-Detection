from flask import Flask, render_template
from datetime import datetime
import grpc
import cv2
import mediapipe as mp
import signData_pb2
import signData_pb2_grpc
import threading

app = Flask(__name__)

webcam_running = True

mp_hands = mp.solutions.hands # mediapipe hands solution
hands = mp_hands.Hands(
    static_image_mode=False,  # Set to False for real-time video tracking
    min_detection_confidence=0.3,  # Confidence threshold for hand detection
    min_tracking_confidence=0.5   # Confidence threshold for maintaining hand tracking
)

def capture_images():
    """Background function to capture images from the webcam."""
    global webcam_running
    cap = cv2.VideoCapture(0)

    while webcam_running:
        ret, frame = cap.read() # ret = capture status (boolean)
        frame_h, frame_w, _ = frame.shape
        hands._image_dimensions = (frame_w, frame_h) # Set Image Dimensions for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converts the frame from BGR (OpenCV's default color format) to RGB (required by MediaPipe)
        normalized_coordinates = []
        temp_x = []
        temp_y = []

        # process captured hands
        results = hands.process(frame_rgb)
        if not ret:
            continue
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    # Extract and append landmarks
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    temp_x.append(x)
                    temp_y.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    # Normalize Coordinates
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    normalized_coordinates.append(x - min(temp_x))
                    normalized_coordinates.append(y - min(temp_y))

                try:
                    with grpc.insecure_channel("localhost:50051") as channel:
                        stub = signData_pb2_grpc.StreamDataServiceStub(channel)
                        response = stub.biDirectionalStream(signData_pb2.RequestMessage(data=normalized_coordinates, timestamp=datetime.now().isoformat()))
                        print(response)
                except Exception as e:
                    print("Error " + e)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    # run webcam in background thread
    webcam_thread = threading.Thread(target=capture_images, daemon=True)
    webcam_thread.start()
    try:
        app.run(debug=True)
    finally:
        webcam_running = False
        webcam_thread.join()