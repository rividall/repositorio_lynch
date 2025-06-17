from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from screens.utils import make_back_button
from core.story_engine import StoryEngine

class StoryScreen(Screen):
    minigame_type_to_screen = {
        "drawing_game": "drawing_game",
        "memory_game": "memory_game",
        "lost_and_found": "lost_and_found",
        "potentiometer_game": "potentiometer_game",
        "color_choice": "color_choice",
        "multiple_choice": "multiple_choice",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.story_engine = None
        self.story_path = None
        self.page_widgets = []
        self.start_minigame_btn = None  # Ensure attribute exists
        self.build_ui()

    def load_story(self, story_path):
        self.story_path = story_path
        self.story_engine = StoryEngine(story_path)
        self.show_page(0)

    def build_ui(self):
        self.clear_widgets()
        self.root = BoxLayout(orientation='vertical', padding=40, spacing=20)
        # Top bar for back button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_level_selection))
        top_bar.add_widget(Label(size_hint=(1, 1)))  # Spacer
        self.root.add_widget(top_bar)
        self.content_box = BoxLayout(orientation='vertical', spacing=20)
        self.root.add_widget(self.content_box)
        # Navigation buttons
        nav_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60, spacing=20)
        self.prev_btn = Button(text="Previous", size_hint=(0.5, 1), font_size=20)
        self.prev_btn.bind(on_release=self.go_previous)
        self.next_btn = Button(text="Next", size_hint=(0.5, 1), font_size=20)
        self.next_btn.bind(on_release=self.go_next)
        nav_box.add_widget(self.prev_btn)
        nav_box.add_widget(self.next_btn)
        self.root.add_widget(nav_box)
        self.add_widget(self.root)
        self.nav_box = nav_box  # Ensure nav_box is accessible in show_page

    def show_page(self, index):
        if not self.story_engine:
            return
        page = self.story_engine.get_page(index)
        self.content_box.clear_widgets()
        if not page:
            self.content_box.add_widget(Label(text="No page found.", font_size=24))
            return
        self.content_box.add_widget(Label(text=page.get("text", ""), font_size=24))
        if "image" in page:
            self.content_box.add_widget(Image(source=page["image"], size_hint=(1, 0.5)))

        # Remove any previous minigame button from nav_box
        if self.start_minigame_btn and self.start_minigame_btn in self.nav_box.children:
            self.nav_box.remove_widget(self.start_minigame_btn)
        self.start_minigame_btn = None

        mini_game = page.get("mini_game")
        if mini_game:
            minigame_type = mini_game.get("type")
            screen_name = self.minigame_type_to_screen.get(minigame_type)
            if screen_name:
                # Hide/disable the Next button, show Start Minigame instead
                self.next_btn.disabled = True
                self.next_btn.opacity = 0
                self.start_minigame_btn = Button(text="Start Minigame", size_hint=(0.5, 1), font_size=20)
                self.start_minigame_btn.bind(on_release=lambda instance: self.start_minigame(screen_name))
                self.nav_box.add_widget(self.start_minigame_btn)
            else:
                self.content_box.add_widget(Label(text=f"Unknown minigame type: {minigame_type}", font_size=18))
                self.next_btn.disabled = False
                self.next_btn.opacity = 1
        else:
            # No minigame, show Next button as normal
            if self.start_minigame_btn and self.start_minigame_btn in self.nav_box.children:
                self.nav_box.remove_widget(self.start_minigame_btn)
            self.start_minigame_btn = None
            self.next_btn.opacity = 1
            if self.story_engine and not self.story_engine.has_next():
                # Last page: Next button becomes "Finish"
                self.next_btn.text = "Finish"
                self.next_btn.disabled = False
            else:
                self.next_btn.text = "Next"
                self.next_btn.disabled = not self.story_engine.has_next()
        self.prev_btn.disabled = not self.story_engine.has_previous()

    def start_minigame(self, screen_name):
        # Set callback for minigame completion
        self.manager.on_minigame_complete = self.on_minigame_complete
        self.manager.current = screen_name

    def on_minigame_complete(self):
        # Advance to next page after minigame and return to story screen
        if self.story_engine and self.story_engine.has_next():
            self.story_engine.next_page()
            self.show_page(self.story_engine.current_index)
            self.manager.current = "story"
        else:
            # If no next page, go to end screen
            self.manager.current = "end"

    def go_next(self, instance):
        if self.story_engine and not self.story_engine.has_next():
            # Last page, finish story
            self.manager.current = "end"
        elif self.story_engine and self.story_engine.has_next():
            self.story_engine.next_page()
            self.show_page(self.story_engine.current_index)

    def go_previous(self, instance):
        if self.story_engine and self.story_engine.has_previous():
            self.story_engine.previous_page()
            self.show_page(self.story_engine.current_index)

    def go_level_selection(self, instance):
        self.manager.current = "level_selection"
