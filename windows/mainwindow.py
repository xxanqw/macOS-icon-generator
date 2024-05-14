from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCheckBox, QMenu, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from os import path as p
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("macOS Icon Generator")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(p.dirname(p.abspath(__file__)) + "icon.icns"))
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 20)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        welcome_label = QLabel("Icon Generator for macOS")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        description_label = QLabel("Usage: Drag and drop an image to the window to generate an icon.\nIcons will be saved in the 'icnoutput' folder.\n\nNote: The image will be automaticly scaled.\nIf you want to generate an ICNS file,\nmake sure you have Xcode Command Line Tools installed.\n\nCreated by @xxanqw.")
        title_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        title_layout.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        
        # Load the base image (icon preview)
        self.base_image_path = p.dirname(p.abspath(__file__)) + "/../img/base.png"
        self.base_image = QPixmap(self.base_image_path)
        self.base_image = self.base_image.scaledToWidth(300)

        # Load the overlay image
        self.overlay_image_path = p.dirname(p.abspath(__file__)) + "/../img/default.png"
        overlay_image = QPixmap(self.overlay_image_path)
        overlay_image = overlay_image.scaled(150, 150)

        painter = QPainter(self.base_image)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Calculate the position where the overlay image should be drawn
        overlay_x = (self.base_image.width() - overlay_image.width()) / 2
        overlay_y = (self.base_image.height() - overlay_image.height()) / 2

        overlay_x = int(overlay_x)
        overlay_y = int(overlay_y)

        # Draw the overlay image at the calculated position
        painter.drawPixmap(overlay_x, overlay_y, overlay_image)
        painter.end()

        # Create a QLabel and set the pixmap to the base image (which now has the overlay image drawn onto it)
        icon_layout = QVBoxLayout()
        self.icon_preview_label = QLabel()
        self.icon_preview_label.setPixmap(self.base_image)
        self.icns_checkbox = QCheckBox("Generate ICNS file")
        self.generate_button = QPushButton("Generate Icon")
        self.generate_button.setStyleSheet("font-size: 16px; padding: 10px 20px; margin-top: 20px; background-color: #007bff; color: white; border: none; border-radius: 5px;")
        self.generate_button.clicked.connect(self.generate_icon)
        icon_layout.addWidget(self.icon_preview_label, alignment=Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(self.icns_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(title_layout)
        layout.addLayout(icon_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)

        self.setCentralWidget(self.central_widget)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        img_path = event.mimeData().urls()[0].toLocalFile()
        # Check if the dropped file is an image
        if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self.load_image(img_path)
        else:
            self.show_message_box("Invalid File", "Please drop a valid image file.\n(.png, .jpg, .jpeg, .bmp)", QMessageBox.Icon.Warning)
        event.acceptProposedAction()

    def load_image(self, path):
        self.user_image_path = path
        self.overlay_image_path = self.user_image_path

        # Load the base image (icon preview)
        base_image_path = p.dirname(p.abspath(__file__)) + "/../img/base.png"
        self.base_image = QPixmap(base_image_path)
        self.base_image = self.base_image.scaledToWidth(300)

        # Load the overlay image
        overlay_image = QPixmap(self.overlay_image_path)
        overlay_image = overlay_image.scaled(150, 150)

        # Create a QPainter instance and draw the overlay image onto the base image
        painter = QPainter(self.base_image)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)  # Enable smooth pixmap transformation

        # Calculate the position where the overlay image should be drawn
        overlay_x = (self.base_image.width() - overlay_image.width()) / 2
        overlay_y = (self.base_image.height() - overlay_image.height()) / 2

        overlay_x = int(overlay_x)
        overlay_y = int(overlay_y)

        # Draw the overlay image at the calculated position
        painter.drawPixmap(overlay_x, overlay_y, overlay_image)
        painter.end()

        # Update the QLabel with the new pixmap
        self.icon_preview_label.setPixmap(self.base_image)

    def generate_icon(self):
        if os.system("which iconutil") != 0 and self.icns_checkbox.isChecked() == True:
            self.show_message_box("XCLTools not found", "iconutil is not installed. Please install Xcode Command Line Tools.", QMessageBox.Icon.Warning)
            return
        from logic.worker import ImageWorker
        worker = ImageWorker(self.base_image_path, self.overlay_image_path, p.dirname(p.abspath(__file__)) + "/../img/icnoutput/icons/icon_512x512@2x.png", self.icns_checkbox.isChecked())
        worker.run()
        self.generate_button.setEnabled(False)
        self.show_message_box("Icon generated", "Icon generated successfully.", QMessageBox.Icon.Information)
        self.generate_button.setEnabled(True)

    def show_message_box(self, title, message, icon=QMessageBox.Icon.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()