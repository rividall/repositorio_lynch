from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from screens.utils import make_back_button
from core.image_manager import ImageManager
from core.video_manager import VideoManager

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subjects = [
            {"name": "Math", "active": True},
            {"name": "Lenguaje", "active": True},
            {"name": "Dibujo", "active": True},
        ]
        self.layout = FloatLayout()  # ✅ This line defines the layout
        self.add_widget(self.layout)

    def on_enter(self):
        self.show_home_image()

    def show_home_image(self):
        self.bg = ImageManager.get_image_widget("home", allow_stretch=True, keep_ratio=False)
        if self.bg:
            self.layout.add_widget(self.bg, index=0)
        self.build_ui()

    def build_ui(self):
        #self.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=40, spacing=20)
        # Top bar for back button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_splash))
        top_bar.add_widget(Label(size_hint=(1, 1)))  # Spacer
        root.add_widget(top_bar)
        # Main content
        root.add_widget(Label(text="Choose a Subject", font_size=28))
        for subj in self.subjects:
            btn = Button(
                text=f"{subj['name']}",
                size_hint=(1, 0.2),
                font_size=22,
                disabled=not subj['active']
            )
            if subj['active']:
                btn.bind(on_release=lambda instance, s=subj['name'].lower(): self.go_level_selection(s))
            root.add_widget(btn)
        # Add Challenges button
        challenges_btn = Button(
            text="Challenges",
            size_hint=(1, 0.2),
            font_size=22,
        )
        challenges_btn.bind(on_release=self.go_challenges)
        root.add_widget(challenges_btn)
        self.add_widget(root)

    def go_level_selection(self, subject):
        # Set the subject on the LevelSelectionScreen and navigate to it
        level_screen = self.manager.get_screen("level_selection")
        level_screen.subject = subject
        level_screen.build_ui()
        self.manager.current = "level_selection"

    def go_challenges(self, instance):
        self.manager.current = "challenge_selection"

    def go_splash(self, instance):
        self.manager.last_screen = "home"
        vm = VideoManager(self.layout)
        vm.play_video("homeTOsplash", on_finish=self.change)

    def change(self):
        self.manager.current = "splash"
