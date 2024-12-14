from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)


model = load_model("emotion_model/emotion_classification_model.h5")
emotion_labels = ['Angry', 'Fear', 'Happy', 'Sad', 'Surprise']


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


emotion_advice = {
    'Angry': "You should take a deep breath and count until 10"
"  How about listening classical music?",
    'Fear': "Are you okay? I think you should just sit and drink water.",
    'Happy': "You can share your happiness with the people you love."
"How about listening to energetic songs?",
    'Sad': "How about sharing your sadness with someone?"
           "You can write and pour your heart out on paper.",
    'Surprise': "You seems surprised.. Is everything OK?"
}


def preprocess_face(face):
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (64, 64))
    face = face / 255.0
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)
    return face


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    def generate_frames():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = frame[y:y + h, x:x + w]
                preprocessed_face = preprocess_face(face)
                prediction = model.predict(preprocessed_face)
                emotion_index = np.argmax(prediction)
                emotion = emotion_labels[emotion_index]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({'success': False, 'message': 'Failed to capture image.'})

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return jsonify({'success': False, 'message': 'No face detected.'})

    (x, y, w, h) = faces[0]
    face = frame[y:y + h, x:x + w]
    preprocessed_face = preprocess_face(face)
    prediction = model.predict(preprocessed_face)
    emotion_index = np.argmax(prediction)
    emotion = emotion_labels[emotion_index]
    advice = emotion_advice[emotion]

    return jsonify({'success': True, 'emotion': emotion, 'advice': advice})


if __name__ == "__main__":
    app.run(debug=True)