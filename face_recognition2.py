import sys
import cv2
import os
import face_recognition
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

# Set plugin path on Linux (skip if you're on Windows)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms"

class FaceMaskApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🧠 Optimized Live Facial Structure Viewer")
        self.setGeometry(100, 100, 900, 750)

        self.video_label = QLabel()
        self.video_label.setFixedSize(800, 600)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #444;")

        self.status_label = QLabel("🔍 Starting camera...")
        self.status_label.setStyleSheet("color: lightgray; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

        # Webcam + timer
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Frame counters and data
        self.frame_count = 0
        self.face_locations = []
        self.face_landmarks_list = []

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("❌ Cannot read from camera")
            return

        self.frame_count += 1
        rgb_frame = frame[:, :, ::-1]

        # Only run face detection every 5th frame
        if self.frame_count % 5 == 0:
            # Resize frame to speed up detection
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
            small_face_locations = face_recognition.face_locations(small_frame)
            small_face_landmarks = face_recognition.face_landmarks(small_frame)

            # Scale back up the locations
            self.face_locations = [
                (top * 2, right * 2, bottom * 2, left * 2)
                for (top, right, bottom, left) in small_face_locations
            ]
            self.face_landmarks_list = []
            for landmarks in small_face_landmarks:
                scaled = {
                    key: [(x * 2, y * 2) for (x, y) in points]
                    for key, points in landmarks.items()
                }
                self.face_landmarks_list.append(scaled)

        # Draw rectangles and landmarks
        for face_landmarks in self.face_landmarks_list:
            for feature_name, points in face_landmarks.items():
                pts = np.array(points, np.int32)
                cv2.polylines(frame, [pts], isClosed=False, color=(0, 255, 0), thickness=2)

                x, y = points[0]
                label = feature_name.replace("_", " ").capitalize()
                cv2.putText(frame, label, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        for (top, right, bottom, left) in self.face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 200, 100), 2)

        # Convert and show on QLabel
        rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_display.shape
        qt_img = QImage(rgb_display.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

        self.status_label.setText(f"🧑 Faces Detected: {len(self.face_locations)}")

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceMaskApp()
    window.show()
    sys.exit(app.exec_())
