A real-time emotion detection system using a custom Convolutional Neural Network (CNN) model, deployed with a Flask-based web application. This project identifies emotions from facial expressions captured via live webcam feeds and provides interactive, emotion-specific feedback.

How It Works
The system uses OpenCV to detect faces in live webcam feeds.
Detected faces are preprocessed (grayscale, resized to 64x64, normalized).
The preprocessed face is fed into the CNN model for emotion classification.
The detected emotion is displayed on the video feed along with actionable advice for the user.


Dataset
https://www.kaggle.com/datasets/eliffirinci/emotions

Technologies Used
- **Programming Languages**: Python, JavaScript
- **Libraries**:
  - TensorFlow/Keras: Deep learning model
  - Flask: Web application
  - OpenCV: Real-time face detection
  - Matplotlib & Seaborn: Visualization
  - NumPy: Data processing
- **Frontend**:
  - HTML/CSS
  - JavaScript for interactivity

Author
Elif FIRINCI

GitHub: https://github.com/elifirinci
