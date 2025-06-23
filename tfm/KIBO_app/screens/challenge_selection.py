from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.utils import make_back_button, fade_in, fade_out
from core.image_manager import ImageManager

MINIGAMES = [
    ("Drawing Game", "drawing_game"),
    ("Memory Game", "memory_game"),
    ("Lost and Found", "lost_and_found"),
    ("Potentiometer Game", "potentiometer_game"),
    ("Color Choice", "color_choice"),
    ("Multiple Choice", "multiple_choice"),
]

class ChallengeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

        self.bg = None

    def on_enter(self):
        self.bg = ImageManager.get_image_widget("challenge_selection", allow_stretch=True, keep_ratio=False)
        self.bg_layout.clear_widgets()
        if self.bg:
            self.bg_layout.add_widget(self.bg)

        self.build_ui()
        fade_in(self.ui_layout)

    def build_ui(self):
        self.ui_layout.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=40, spacing=20)
        # Top bar for back button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_home))
        top_bar.add_widget(Label(size_hint=(1, 1)))  # Spacer
        root.add_widget(top_bar)
        # Main content
        root.add_widget(Label(text="Select a Challenge"))
        from core.utils import home_button
        for label_text, screen_name in MINIGAMES:
            btn = home_button(
                "desafiobtn",
                0, 0, 600, 120,  # width/height can be adjusted as needed
                label_text,
                lambda instance, s=screen_name: self.launch_minigame(s)
            )
            btn.pos_hint = {'center_x': 0.5}
            root.add_widget(btn)
        self.ui_layout.add_widget(root)

    def launch_minigame(self, screen_name):
        # Set a flag so the minigame knows to return here
        self.manager.challenge_mode = True
        self.manager.last_screen = "challenge_selection"
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", screen_name))

    def go_home(self, instance):
        self.manager.last_screen = "challenge_selection"
        self.manager.next_screen = "home"
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))
