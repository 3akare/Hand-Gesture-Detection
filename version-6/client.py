from flask import Flask, render_template, jsonify
from datetime import datetime
import grpc
import cv2
import mediapipe as mp
import signData_pb2
import signData_pb2_grpc
import threading

app = Flask(__name__)

webcam_running = False  # Initially set to False
webcam_thread = None
collected_gestures = []  # Store hand gesture arrays here
lock = threading.Lock()  # Thread-safe lock
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
                with lock:
                    collected_gestures.append(normalized_coordinates)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start():
    global webcam_running, webcam_thread
    if not webcam_running:
        webcam_running = True
        webcam_thread = threading.Thread(target=capture_images, daemon=True)
        webcam_thread.start()
        return jsonify({"status": "Webcam started"})
    return jsonify({"status": "Webcam already running"})

@app.route('/send', methods=['POST'])
def send():
    global webcam_running, webcam_thread, collected_gestures

    # Stop webcam
    if webcam_running:
        webcam_running = False
        webcam_thread.join()

    # Check if collected gestures is empty
    with lock:
        if not collected_gestures:
            return jsonify({"status": "No gestures to send"})
        data_to_send = collected_gestures[:]
        collected_gestures = []

    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            gestures = [signData_pb2.Gesture(points=gesture) for gesture in data_to_send]
            stub = signData_pb2_grpc.StreamDataServiceStub(channel)
            response = stub.biDirectionalStream(
                signData_pb2.RequestMessage(
                    data=gestures,
                    timestamp=datetime.now().isoformat()
                )
            )
            return jsonify({"status": "Data sent successfully", "response": response.reply})
    except Exception as e:
        print(e)
    return jsonify({"status": "Good"})

@app.route('/stop', methods=['POST'])
def stop_webcam():
    global webcam_running, webcam_thread
    if webcam_running:
        webcam_running = False
        webcam_thread.join()
        return jsonify({"status": "Webcam stopped"})
    return jsonify({"status": "Webcam is not running"})

if __name__ == '__main__':
    app.run(debug=True)
