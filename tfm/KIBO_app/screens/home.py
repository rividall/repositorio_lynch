from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from core.utils import fade_out, fade_in, home_button, make_back_button
from core.audio_manager import AudioManager
from core.image_manager import ImageManager
from core.video_manager import VideoManager
import os
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subjects = [
            {"name": "Matemáticas", "active": True},
            {"name": "Lenguaje", "active": True},
            {"name": "Dibujo", "active": True},
        ]

        # Separate layouts for background and UI
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

        self.bg = None

    def on_enter(self):
        self.bg = ImageManager.get_image_widget("home", allow_stretch=True, keep_ratio=False)
        self.bg_layout.add_widget(self.bg)
        self.build_ui()
        fade_in(self.ui_layout)

    
    def build_ui(self):
        self.ui_layout.clear_widgets()
        root = FloatLayout()

        # Back button
        root.add_widget(make_back_button(self.go_splash))
        # Subject buttons
        root.add_widget(home_button("btnMatemáticas", 0.49, 0.42, 400, 400,
                                    lambda instance: self.go_level_selection("matemáticas")))
        root.add_widget(home_button("btnLenguaje", 0.15, 0.67, 420, 450,
                                    lambda instance: self.go_level_selection("lenguaje")))
        root.add_widget(home_button("btnDesafio", 0.52, 0.06, 460, 450,
                                    lambda instance: self.go_challenges(instance)))

        self.ui_layout.add_widget(root)


    
    def go_level_selection(self, subject):
        self.manager.last_screen = "home"
        self.manager.next_screen = "level_selection"
        self.manager.next_subject = subject  # ✅ Set for switch screen
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))

    def go_challenges(self, instance):
        self.manager.last_screen = "home"
        self.manager.next_screen = "challenge_selection"
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))

    def go_splash(self, instance):
        self.manager.last_screen = "home"
        self.manager.next_screen = "splash"
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))

    def change(self):
        self.manager.current = "splash"
