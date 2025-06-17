from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from screens.utils import make_back_button

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=40, spacing=20)
        # Top bar for back button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_minigame))
        top_bar.add_widget(Label(size_hint=(1, 1)))  # Spacer
        root.add_widget(top_bar)
        # Main content
        root.add_widget(Label(text="End Screen", font_size=28))
        btn = Button(text="Back to selection", size_hint=(1, 0.2), font_size=22)
        btn.bind(on_release=self.go_level_selection)
        root.add_widget(btn)
        self.add_widget(root)

    def go_level_selection(self, instance):
        self.manager.current = "level_selection"

    def go_minigame(self, instance):
        self.manager.current = "minigame"
