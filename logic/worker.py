from PyQt6.QtCore import QThread, pyqtSignal
from logic.image_generation import generate_image
from logic.image_resize import resize
from logic.move import move
from os import path as p

class ImageWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, background_path, overlay_path, output_path, icns_is_checked):
        super().__init__()
        self.background_path = background_path
        self.overlay_path = overlay_path
        self.output_path = output_path
        self.icns_is_checked = icns_is_checked

    def run(self):
        # Perform your background task here
        # This will run in a separate thread
        generate_image(self.background_path, self.overlay_path, self.output_path, overlay_resize=(512, 512))
        resize()
        if self.icns_is_checked == True:
            from logic.image_bundle import create_icns
            self.icns = [
                self.output_path.replace("512x512@2x", "16x16"),
                self.output_path.replace("512x512@2x", "16x16@2x"),
                self.output_path.replace("512x512@2x", "32x32"),
                self.output_path.replace("512x512@2x", "32x32@2x"),
                self.output_path.replace("512x512@2x", "128x128"),
                self.output_path.replace("512x512@2x", "128x128@2x"),
                self.output_path.replace("512x512@2x", "256x256"),
                self.output_path.replace("512x512@2x", "256x256@2x"),
                self.output_path.replace("512x512@2x", "512x512"),
                self.output_path
            ]
            create_icns(self.icns, "icon.icns")
        move()

        # Emit the finished signal when the task is done
        self.finished.emit()