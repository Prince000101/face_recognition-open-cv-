import os
import sys
import cv2
import numpy as np
import face_recognition
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve

# Set environment variables for Qt
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms'


class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition Security System")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize variables
        self.known_face_encoding = None
        self.capture = None
        self.timer = QTimer()
        self.process_this_frame = True
        self.face_detected = False
        self.current_frame = None
        self.saved_face_preview = None

        # Setup UI
        self.setup_ui()

        # Start camera
        self.start_camera()

    def setup_ui(self):
        """Initialize all UI components"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # Camera feed (left side)
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: black;")
        self.main_layout.addWidget(self.camera_label, 60)  # 60% width

        # Right panel
        right_panel = QVBoxLayout()

        # Saved face preview
        self.face_preview_label = QLabel("No face saved")
        self.face_preview_label.setAlignment(Qt.AlignCenter)
        self.face_preview_label.setFixedSize(150, 150)
        self.face_preview_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border: 2px dashed #aaaaaa;
                border-radius: 5px;
            }
        """)
        right_panel.addWidget(self.face_preview_label, 0, Qt.AlignCenter)

        # Save face button
        self.save_face_button = QPushButton("Save Current Face")
        self.save_face_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.save_face_button.clicked.connect(self.save_current_face)
        right_panel.addWidget(self.save_face_button)

        # Load face button
        self.load_face_button = QPushButton("Load Face Image")
        self.load_face_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.load_face_button.clicked.connect(self.load_face_image)
        right_panel.addWidget(self.load_face_button)

        # Lock animation
        self.lock_animation = LockAnimation()
        right_panel.addWidget(self.lock_animation, 0, Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Ready - Capture or load a face to begin")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        right_panel.addWidget(self.status_label)

        # Quit button
        quit_button = QPushButton("Quit")
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        quit_button.clicked.connect(self.close)
        right_panel.addWidget(quit_button)

        # Add right panel to main layout
        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel)
        right_panel_widget.setStyleSheet("background-color: #f0f0f0;")
        self.main_layout.addWidget(right_panel_widget, 40)  # 40% width

    def save_current_face(self):
        """Save the current face from camera"""
        if self.current_frame is None:
            return

        try:
            # Convert to RGB
            rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)

            # Find faces in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)

            if not face_locations:
                self.status_label.setText("No face detected in frame!")
                self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                return

            # Get the first face found
            top, right, bottom, left = face_locations[0]
            face_image = rgb_frame[top:bottom, left:right]

            # Save the face image
            save_path = "saved_face.jpg"
            cv2.imwrite(save_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))

            # Update the preview
            self.update_face_preview(face_image)

            # Load the face encoding
            self.load_known_face(save_path)

            self.status_label.setText("Face saved successfully!")
            self.status_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")

        except Exception as e:
            self.status_label.setText(f"Error saving face: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
            print(f"Error saving face: {e}")

    def load_face_image(self):
        """Load a face image from file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open Face Image", "", "Image Files (*.jpg *.jpeg *.png)"
            )

            if file_path:
                # Load and display the image
                image = face_recognition.load_image_file(file_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Find faces in the image
                face_locations = face_recognition.face_locations(rgb_image)

                if not face_locations:
                    self.status_label.setText("No face found in the image!")
                    self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                    return

                # Get the first face found
                top, right, bottom, left = face_locations[0]
                face_image = rgb_image[top:bottom, left:right]

                # Update the preview
                self.update_face_preview(face_image)

                # Save a copy
                save_path = "loaded_face.jpg"
                cv2.imwrite(save_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))

                # Load the face encoding
                self.load_known_face(save_path)

                self.status_label.setText("Face loaded successfully!")
                self.status_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")

        except Exception as e:
            self.status_label.setText(f"Error loading face: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
            print(f"Error loading face: {e}")

    def update_face_preview(self, face_image):
        """Update the face preview with the given image"""
        try:
            # Convert to QImage
            h, w, ch = face_image.shape
            bytes_per_line = ch * w
            q_img = QImage(face_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Scale and display
            self.face_preview_label.setPixmap(
                QPixmap.fromImage(q_img).scaled(
                    self.face_preview_label.width(),
                    self.face_preview_label.height(),
                    Qt.KeepAspectRatio
                )
            )
            self.face_preview_label.setStyleSheet("border: 2px solid #4CAF50;")

        except Exception as e:
            print(f"Error updating face preview: {e}")

    def load_known_face(self, image_path):
        """Load the known face encoding"""
        try:
            # Load image file
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Could not find face image at {image_path}")

            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                raise ValueError("No faces found in the provided image")

            self.known_face_encoding = face_encodings[0]
            self.status_label.setText("Ready - Waiting for face...")
            self.status_label.setStyleSheet("color: black; font-size: 18px; font-weight: bold;")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
            print(f"Error loading face: {e}")

    def start_camera(self):
        """Initialize and start camera capture"""
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise RuntimeError("Could not open camera")

            # Start timer for frame updates
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # ~30 FPS

        except Exception as e:
            self.status_label.setText(f"Camera Error: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
            print(f"Camera error: {e}")

    def update_frame(self):
        """Process each camera frame"""
        try:
            ret, frame = self.capture.read()
            if not ret:
                return

            # Store the current frame for saving
            self.current_frame = frame.copy()

            # Process every other frame to save CPU
            if self.process_this_frame and self.known_face_encoding is not None:
                # Resize and convert color
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB

                # Find all faces
                face_locations = face_recognition.face_locations(rgb_small_frame)

                if face_locations:
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    for face_encoding in face_encodings:
                        # Compare with known face
                        matches = face_recognition.compare_faces(
                            [self.known_face_encoding],
                            face_encoding,
                            tolerance=0.6  # Adjust tolerance as needed
                        )

                        if True in matches:
                            if not self.face_detected:
                                self.face_detected = True
                                self.lock_animation.toggle_lock(False)
                                self.status_label.setText("Authorized: Access Granted!")
                                self.status_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
                        else:
                            if self.face_detected:
                                self.face_detected = False
                                self.lock_animation.toggle_lock(True)
                                self.status_label.setText("Unauthorized: Access Denied")
                                self.status_label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                else:
                    if self.face_detected:
                        self.face_detected = False
                        self.lock_animation.toggle_lock(True)
                        self.status_label.setText("Waiting for face...")
                        self.status_label.setStyleSheet("color: black; font-size: 18px; font-weight: bold;")

            self.process_this_frame = not self.process_this_frame

            # Display the frame
            self.display_frame(frame)

        except Exception as e:
            print(f"Frame processing error: {e}")

    def display_frame(self, frame):
        """Convert and display the OpenCV frame in Qt"""
        try:
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create QImage
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Scale and display
            self.camera_label.setPixmap(
                QPixmap.fromImage(q_img).scaled(
                    self.camera_label.width(),
                    self.camera_label.height(),
                    Qt.KeepAspectRatio
                )
            )
        except Exception as e:
            print(f"Display error: {e}")

    def closeEvent(self, event):
        """Clean up resources when closing"""
        if self.capture and self.capture.isOpened():
            self.capture.release()
        if self.timer.isActive():
            self.timer.stop()
        event.accept()


class LockAnimation(QLabel):
    """Custom widget for lock/unlock animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.locked = True
        self.setFixedSize(300, 300)
        self.lock_color = QColor(255, 0, 0)  # Red
        self.unlock_color = QColor(0, 255, 0)  # Green
        self.current_color = self.lock_color
        self.animation = None
        self.setAlignment(Qt.AlignCenter)

        self.font = QFont()
        self.font.setPointSize(24)
        self.font.setBold(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw outer circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.current_color)
        painter.drawEllipse(10, 10, 280, 280)

        # Draw inner circle
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(50, 50, 200, 200)

        # Draw lock/unlock symbol
        if self.locked:
            painter.setPen(QPen(QColor(0, 0, 0), 5))
            painter.drawRect(120, 130, 60, 70)
            painter.drawEllipse(135, 110, 30, 30)
            painter.setFont(self.font)
            painter.drawText(QRect(0, 220, 300, 50), Qt.AlignCenter, "LOCKED")
        else:
            painter.setPen(QPen(QColor(0, 0, 0), 5))
            painter.drawRect(120, 130, 60, 70)
            painter.drawArc(135, 110, 30, 30, 0, 180 * 16)
            painter.setFont(self.font)
            painter.drawText(QRect(0, 220, 300, 50), Qt.AlignCenter, "UNLOCKED")

    def toggle_lock(self, locked):
        self.locked = locked
        self.current_color = self.lock_color if locked else self.unlock_color

        if self.animation:
            self.animation.stop()

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setStartValue(QRect(self.x(), self.y(), 280, 280))
        self.animation.setEndValue(QRect(self.x(), self.y(), 300, 300))
        self.animation.start()
        self.update()


if __name__ == "__main__":
    # Configure environment
    if 'QT_QPA_PLATFORM_PLUGIN_PATH' not in os.environ:
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins'

    # Create application
    app = QApplication(sys.argv)

    try:
        app.setStyle("Fusion")
    except:
        pass

    # Create and show main window
    window = FaceRecognitionApp()
    window.show()

    # Run application
    sys.exit(app.exec_())