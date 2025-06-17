from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from screens.utils import make_back_button
from core.story_engine import list_available_stories
import os
class LevelSelectionScreen(Screen):
    def __init__(self, subject="math", **kwargs):
        super().__init__(**kwargs)
        self.subject = subject
        self.story_buttons = []
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
        root.add_widget(Label(text=f"Select a {self.subject.capitalize()} Story", font_size=28))
        # Construct absolute path to story folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        story_dir = os.path.normpath(os.path.join(current_dir, "..", "stories", self.subject))

        stories = list_available_stories(f"stories/{self.subject}")
        if not stories:
            root.add_widget(Label(text="No stories found.", font_size=20))
        else:
            for story in stories:
                btn = Button(
                    text=story["title"],
                    size_hint=(1, 0.2),
                    font_size=22
                )
                btn.bind(on_release=lambda instance, s=story: self.go_story(s["filename"]))
                root.add_widget(btn)
                self.story_buttons.append(btn)
        self.add_widget(root)

    def go_story(self, story_filename):
        # Pass the selected story file to the StoryScreen
        story_path = f"stories/{self.subject}/{story_filename}"
        self.manager.get_screen("story").load_story(story_path)
        self.manager.current = "story"

    def go_home(self, instance):
        self.manager.current = "home"

    def on_pre_enter(self, *args):
        # Rebuild UI in case subject has changed
        self.build_ui()
