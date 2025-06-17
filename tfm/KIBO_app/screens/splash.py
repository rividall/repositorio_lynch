from kivy.uix.screenmanager import Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.audio_manager import AudioManager
from core.video_manager import VideoManager
from core.image_manager import ImageManager

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Add background image
        self.bg = ImageManager.get_image_widget("splash", allow_stretch=True, keep_ratio=False)
        if self.bg:
            self.layout.add_widget(self.bg, index=0)

        self.logo_img = ImageManager.get_image_widget("logo", size_hint=(None, None), size=(800, 300), pos_hint={"center_x": 0.5, "center_y": 0.8})
        if self.logo_img:
            self.layout.add_widget(self.logo_img)

    def on_enter(self):
        AudioManager.get_instance().start_background_music()
        VideoManager.preload_video("splashTOhome")
        
    def on_touch_down(self, touch):
        vm = VideoManager(self.layout)
        vm.play_video("splashTOhome", on_finish=self.go_home, use_preloaded=True)
        return True

    def go_home(self, *args):
        self.manager.last_screen = "splash"  # Track current before switching
        self.manager.current = "home"