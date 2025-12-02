import cv2
import easyocr
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import numpy as np
import os

# Initialize EasyOCR for English and Hindi
reader = easyocr.Reader(['en', 'hi'])

class HandwritingRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Handwritten Text Recognition")
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #171e30;
            }
            QTextEdit {
                background-color: #131c31;
                color: #d4d6ff;
                border: 4px solid #5c6bff;
                border-radius: 15px;
                font: 22pt 'Trebuchet MS';
            }
            QPushButton#load_image_button,
            QPushButton#exit_button {
                background-color: #8292ff;
                color: #1f283e;
                font: 16pt 'Trebuchet MS';
                border: none;
                border-radius: 10px;
                margin: 5px 2px;
                padding: 10px 50px;
            }
            QPushButton#load_image_button:hover,
            QPushButton#exit_button:hover {
                background-color: #98a4ff;
            }
            QLabel {
                background-color: #1e1e2e;
                border: 1px solid #6272a4;
            }
        """)
        self.current_image = None
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.image_layout = QVBoxLayout()
        self.text_layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)
        self.image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.text_field = QTextEdit(self)
        self.text_field.setReadOnly(True)
        self.text_layout.addWidget(self.text_field)

        buttons_layout = QHBoxLayout()

        self.load_image_button = QPushButton("Load Image", self)
        self.load_image_button.setObjectName("load_image_button")
        self.load_image_button.setFixedSize(250, 60)
        self.load_image_button.clicked.connect(self.load_image)
        buttons_layout.addWidget(self.load_image_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setFixedSize(250, 60)
        self.exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.exit_button)

        self.text_layout.addLayout(buttons_layout)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.text_layout)
        self.central_widget.setLayout(self.main_layout)

    def recognize_text(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray, allowlist=None, detail=1)
        recognized_text = ""

        for (bbox, text, _) in results:
            pts = np.array(bbox, dtype=np.int32)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(frame, text, (pts[0][0], pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 5)
            recognized_text += text + ' '

        self.text_field.clear()
        self.text_field.append(recognized_text.strip())
        return frame

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                  "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name and os.path.isfile(file_name):
            self.current_image = cv2.imread(file_name)
            if self.current_image is None:
                QMessageBox.critical(self, "Error", "Failed to load image. Check file format.")
                return

            frame = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            frame_with_boxes = self.recognize_text(frame)

            h, w, ch = frame_with_boxes.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_with_boxes.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qt_pixmap = qt_image.scaled(640, 480, Qt.KeepAspectRatio)
            self.image_label.setPixmap(QPixmap.fromImage(qt_pixmap))
        else:
            QMessageBox.warning(self, "No File", "No image file selected or file does not exist.")

    def closeEvent(self, event):
        # Removed cv2.destroyAllWindows() to avoid OpenCV GUI errors in PyQt-only apps
        event.accept()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandwritingRecognitionApp()
    window.show()
    sys.exit(app.exec_())
