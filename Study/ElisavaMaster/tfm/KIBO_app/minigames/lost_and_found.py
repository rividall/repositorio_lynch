from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from core.utils import fade_in, fade_out
from core.image_manager import ImageManager
from core.audio_manager import AudioManager
class LostAndFoundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)
        self.bg = None
        self.label = None
        self.continue_btn = None

    def on_enter(self):
        self.bg_layout.clear_widgets()
        self.ui_layout.clear_widgets()
        # Use a placeholder background image, replace with relevant one if needed
        self.bg = ImageManager.get_image_widget("lf1", allow_stretch=True, keep_ratio=False)
        if self.bg:
            self.bg_layout.add_widget(self.bg)
        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)

    def build_ui(self):
        from core.utils import make_back_button
        # Back button (top left)
        back_btn = make_back_button(self.go_back)
        self.ui_layout.add_widget(back_btn)

        # Label at the top
        self.label = Label(
            text="¿Donde está KIBO?",
            font_size=98,
            color=(1,1,1,1),
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'top': 0.98},
            halign="center",
            valign="top"
        )
        self.label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
        self.ui_layout.add_widget(self.label)

        # Transparent, textless button at x=0.5, y=0.4
        self.continue_btn = Button(
            text="",
            background_normal='',
            background_color=(0,0,0,0),
            size_hint=(0.12, 0.1),
            pos_hint={'x': 0.49, 'y': 0.03},
            on_release=self.complete_game
        )
        self.ui_layout.add_widget(self.continue_btn)

    def go_back(self, instance):
        def switch_screen():
            last = getattr(self.manager, "last_screen", None)
            if last == "story":
                self.manager.current = "story"
            else:
                self.manager.current = "challenge_selection"
        fade_out(self.ui_layout, on_complete=switch_screen)

    def complete_game(self, instance):
        AudioManager.get_instance().play_sound_effect("correct")
        def switch_screen():
            if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
                self.manager.challenge_mode = False
                self.manager.current = "challenge_selection"
            elif hasattr(self.manager, "on_minigame_complete"):
                self.manager.on_minigame_complete()
            else:
                self.manager.current = "story"
        fade_out(self.ui_layout, on_complete=switch_screen)
