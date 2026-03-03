from kivy.uix.screenmanager import Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.utils import fade_out, fade_in
from core.audio_manager import AudioManager
from core.video_manager import VideoManager
from core.image_manager import ImageManager

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Separate background and UI layouts
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

        # Add background image
        self.bg = ImageManager.get_image_widget("splash", allow_stretch=True, keep_ratio=False)
        self.bg_layout.add_widget(self.bg)

    def on_enter(self):
        AudioManager.get_instance().start_background_music()

        # Add logo to UI layout
        #self.logo_img = ImageManager.get_image_widget("logo", size_hint=(None, None), size=(400, 300), pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.logo_img = ImageManager.get_image_widget(
            "logo",
            size_hint=(0.8, 0.5),  # 40% of width, 30% of height
            pos_hint={"center_x": 0.5, "center_y": 0.8}
        )
        self.ui_layout.add_widget(self.logo_img)
        #self.ui_layout.add_widget(Label(text="Presiona para \ncomenzar",halign='center')) #CALL TO ACTION
        label = Label(
            text="Presiona para \ncomenzar",
            halign='center',
            valign='bottom',
            size_hint=(1, None),
            height=100,
            pos_hint={"center_x": 0.5, "y": 0.1}
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        self.ui_layout.add_widget(label)

        fade_in(self.ui_layout)

    def on_touch_down(self, touch):
        AudioManager.get_instance().play_sound_effect("click")
        self.go_home()
        return True

    def go_home(self, *args):
        self.manager.last_screen = "splash"
        self.manager.next_screen = "home"
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))
