from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.utils import make_back_button, fade_in, fade_out
from core.story_engine import list_available_stories
from core.image_manager import ImageManager
from core.audio_manager import AudioManager

import os

class LevelSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.story_buttons = []

        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

        self.bg = None

    def on_pre_enter(self, *args):
        #self.subject = getattr(self, "subject", "matemáticas")  # Make sure it's up to date
        self.subject = getattr(self.manager, "next_subject", None)
        self.load_background()
        AudioManager.get_instance().change_background_music("background")
        self.build_ui()
        fade_in(self.ui_layout)

    def load_background(self):
        self.bg_layout.clear_widgets()
        self.bg = ImageManager.get_image_widget(self.subject, allow_stretch=True, keep_ratio=False)
        if self.bg:
            self.bg_layout.add_widget(self.bg)

    def build_ui(self):
        self.ui_layout.clear_widgets()
        root = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_home))
        top_bar.add_widget(Label(size_hint=(1, 1)))
        root.add_widget(top_bar)

        # Title
        root.add_widget(Label(text=f"Elige una historia \nde {self.subject.capitalize()}"))

        # Stories
        stories = list_available_stories(f"stories/{self.subject}")
        if not stories:
            root.add_widget(Label(text="No stories found.", font_size=20))
        else:
            for story in stories:
                btn = Button(
                    text=story["title"],
                    size_hint=(1, 0.2),
                    font_size=62
                )
                btn.bind(on_release=lambda instance, s=story: self.go_story(s["filename"]))
                root.add_widget(btn)
                self.story_buttons.append(btn)

        self.ui_layout.add_widget(root)

    def go_story(self, story_filename):
        story_path = f"stories/{self.subject}/{story_filename}"
        self.manager.get_screen("story").load_story(story_path)
        self.manager.last_screen = "level_selection"
        self.manager.next_screen = "story"
        fade_out(self.bg_layout)
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "story"))

    def go_home(self, instance):
        self.manager.last_screen = "level_selection"
        self.manager.next_screen = "home"
        self.manager.next_subject = self.subject  # ✅ Pass subject
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "switch"))
