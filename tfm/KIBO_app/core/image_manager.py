
import os
from kivy.uix.image import Image

class ImageManager:
    @staticmethod
    def get_image_widget(image_name, **kwargs):
        image_map = {
            "home": "home.png",
            "splash": "splash.png",
            "logo": "logo.png",
            # Add more mappings as needed
        }

        filename = image_map.get(image_name)
        if not filename:
            print(f"⚠️ Unknown image: '{image_name}'")
            return None

        # Absolute path resolution
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.normpath(os.path.join(current_dir, "..", "assets", "images"))
        path = os.path.join(image_dir, filename)

        if not os.path.exists(path):
            print(f"⚠️ Image file not found: {path}")
            return None

        return Image(source=path, **kwargs)
