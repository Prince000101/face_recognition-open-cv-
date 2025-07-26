import sys
import os
import cv2
import face_recognition
import numpy as np
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

# Force Qt to use correct platform plugin
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms'


class FaceCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🪪 Passport Photo Capture")
        self.setGeometry(100, 100, 900, 750)

        # 🖼️ Live camera feed
        self.image_label = QLabel()
        self.image_label.setFixedSize(800, 600)
        self.image_label.setStyleSheet("background-color: black; border: 2px solid #444;")

        # 📍 Status label
        self.status_label = QLabel("📷 Waiting for faces...")
        self.status_label.setStyleSheet("color: lightgray; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # ⏺️ Capture button
        self.capture_button = QPushButton("📸 Capture Passport Photos")
        self.capture_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7; color: white;
                font-size: 18px; padding: 12px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.capture_button.clicked.connect(self.capture_faces)

        # 🧱 Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")

        # 📷 Camera + timer
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.latest_frame = None
        self.face_locations = []

        # 📁 Output folder
        self.output_dir = "captured_passport_faces"
        os.makedirs(self.output_dir, exist_ok=True)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.latest_frame = frame.copy()
        rgb_frame = frame[:, :, ::-1]  # BGR to RGB

        self.face_locations = face_recognition.face_locations(rgb_frame)

        # 🟩 Draw green boxes around all faces
        for (top, right, bottom, left) in self.face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display number of faces
        self.status_label.setText(f"🧑 Detected Faces: {len(self.face_locations)}")

        # Convert frame to Qt image
        rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_display.shape
        qt_img = QImage(rgb_display.data, w, h, ch * w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    def capture_faces(self):
        if self.latest_frame is None or not self.face_locations:
            self.status_label.setText("⚠️ No faces detected to capture!")
            return

        count = 0
        h, w, _ = self.latest_frame.shape
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        for (top, right, bottom, left) in self.face_locations:
            # 📐 Expand face to passport region
            margin_y = int((bottom - top) * 1.2)
            margin_x = int((right - left) * 0.5)

            new_top = max(0, top - margin_y)
            new_bottom = min(h, bottom + margin_y // 3)
            new_left = max(0, left - margin_x)
            new_right = min(w, right + margin_x)

            face_img = self.latest_frame[new_top:new_bottom, new_left:new_right]

            # Resize to standard digital passport format
            passport_size = cv2.resize(face_img, (350, 450))

            filename = f"{self.output_dir}/passport_{timestamp}_{count + 1}.jpg"
            cv2.imwrite(filename, passport_size)
            count += 1

        self.status_label.setText(f"✅ Saved {count} passport photo(s)!")

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceCaptureApp()
    window.show()
    sys.exit(app.exec_())
