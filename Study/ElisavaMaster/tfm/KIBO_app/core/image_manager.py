import os
from kivy.uix.image import Image

class ImageManager:
    @staticmethod
    def get_image_widget(image_name, **kwargs):
        # Directly construct filename
        filename = f"{image_name}.png"

        # Absolute path resolution
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.normpath(os.path.join(current_dir, "..", "assets", "images"))
        path = os.path.join(image_dir, filename)

        if not os.path.exists(path):
            #print(f"⚠️ Image file not found: {path}")
            return None

        return Image(source=path, **kwargs)
