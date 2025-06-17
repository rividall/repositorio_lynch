from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class PotentiometerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="Potentiometer Game (placeholder)", font_size=28))
        complete_btn = Button(text="Complete Potentiometer Game", size_hint=(1, 0.2), font_size=22)
        complete_btn.bind(on_release=self.complete_game)
        layout.add_widget(complete_btn)
        self.add_widget(layout)

    def complete_game(self, instance):
        if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
            self.manager.challenge_mode = False
            self.manager.current = "challenge_selection"
        elif hasattr(self.manager, "on_minigame_complete"):
            self.manager.on_minigame_complete()
        else:
            self.manager.current = "story"