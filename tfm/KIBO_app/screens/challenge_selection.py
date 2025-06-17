from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from screens.utils import make_back_button

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
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=40, spacing=20)
        # Top bar for back button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_home))
        top_bar.add_widget(Label(size_hint=(1, 1)))  # Spacer
        root.add_widget(top_bar)
        # Main content
        root.add_widget(Label(text="Select a Challenge", font_size=28))
        for label_text, screen_name in MINIGAMES:
            btn = Button(text=label_text, size_hint=(1, 0.2), font_size=22)
            btn.bind(on_release=lambda instance, s=screen_name: self.launch_minigame(s))
            root.add_widget(btn)
        self.add_widget(root)

    def launch_minigame(self, screen_name):
        # Set a flag so the minigame knows to return here
        self.manager.challenge_mode = True
        self.manager.current = screen_name

    def go_home(self, instance):
        self.manager.current = "home"