from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from core.utils import make_back_button, make_forward_button,  fade_in, fade_out
from core.story_engine import StoryEngine
from core.audio_manager import AudioManager
from core.image_manager import ImageManager

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
        self.start_minigame_btn = None

        self.bg_layout = FloatLayout()
        self.ui_layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

    def load_story(self, story_path):
        self.story_path = story_path
        self.story_engine = StoryEngine(story_path)
        self.subject = getattr(self.manager, "next_subject", None)  # ✅ use manager
        AudioManager.get_instance().change_background_music(self.subject)
        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)
        self.show_page(0)

    def build_ui(self):
        self.ui_layout.clear_widgets()
        self.content_box = BoxLayout(orientation='vertical', spacing=20)

        # Top bar for back button
        from core.utils import home_button

        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
        top_bar.add_widget(make_back_button(self.go_level_selection, text="Salir"))
        top_bar.add_widget(Label(size_hint=(1, 1)))
        self.ui_layout.add_widget(top_bar)
        self.ui_layout.add_widget(self.content_box)

        # Navigation buttons
        nav_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60, spacing=20)
        self.prev_btn = home_button("backArrow", 0, 0, 170, 140, "Volver", self.go_previous)
        self.next_btn = make_forward_button(self.go_next, text="Seguir")
        nav_box.add_widget(self.prev_btn)
        from kivy.uix.label import Label as KivyLabel
        nav_box.add_widget(KivyLabel(size_hint_x=1))
        nav_box.add_widget(self.next_btn)
        self.ui_layout.add_widget(nav_box)
        self.nav_box = nav_box

    def show_page(self, index):
        if not self.story_engine:
            return
        page = self.story_engine.get_page(index)
        self.content_box.clear_widgets()
        self.bg_layout.clear_widgets()

        if not page:
            self.content_box.add_widget(Label(text="No page found.", font_size=24))
            return

        # Background image
        bg_name = f"{self.subject}_story"
        bg = ImageManager.get_image_widget(bg_name, allow_stretch=True, keep_ratio=False)
        if bg:
            self.bg_layout.add_widget(bg)

        # Personalized page image
        page_img_name = f"{self.subject}page{self.story_engine.current_index + 1}"
        page_img = ImageManager.get_image_widget(page_img_name, size_hint=(None, None), size=(300, 300), pos=(100, 150))
        if page_img:
            self.bg_layout.add_widget(page_img)

        # Story text
        text_label = Label(
            text=page.get("text", ""),
            font_size=64,
            size_hint=(0.8, 0.8),
            pos_hint={'x': 0.1, 'y': 0.1},
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        )

        def fit_text(instance, *_):
            # Dynamically adjust font size so text fits in bounding box
            max_width = instance.width
            max_height = instance.height
            font_size = 64
            instance.font_size = font_size
            instance.text_size = (max_width, None)
            instance.texture_update()
            while (instance.texture_size[0] > max_width or instance.texture_size[1] > max_height) and font_size > 10:
                font_size -= 2
                instance.font_size = font_size
                instance.text_size = (max_width, None)
                instance.texture_update()
            instance.text_size = (max_width, max_height)

        text_label.bind(size=fit_text, text=fit_text)
        self.bg_layout.add_widget(text_label)
        # Initial fit
        fit_text(text_label)

        # Page image from story (optional)
        #if "image" in page:
        #    self.content_box.add_widget(Image(source=page["image"], size_hint=(1, 0.5)))

        if self.start_minigame_btn and self.start_minigame_btn in self.nav_box.children:
            self.nav_box.remove_widget(self.start_minigame_btn)
        self.start_minigame_btn = None

        mini_game = page.get("mini_game")
        if mini_game:
            minigame_type = mini_game.get("type")
            screen_name = self.minigame_type_to_screen.get(minigame_type)
            if screen_name:
                self.next_btn.disabled = True
                self.next_btn.opacity = 0
                from core.utils import home_button
                btn_width = 500
                self.start_minigame_btn = home_button(
                    f"{self.subject}btn",
                    0, 0, btn_width, 120,
                    "Start Minigame",
                    lambda instance: self.start_minigame(screen_name)
                )
                self.start_minigame_btn.pos_hint = {'center_x': 0.5}
                self.nav_box.add_widget(self.start_minigame_btn)
            else:
                self.content_box.add_widget(Label(text=f"Unknown minigame type: {minigame_type}", font_size=18))
                self.next_btn.disabled = False
                self.next_btn.opacity = 1
        else:
            if self.start_minigame_btn and self.start_minigame_btn in self.nav_box.children:
                self.nav_box.remove_widget(self.start_minigame_btn)
            self.start_minigame_btn = None
            self.next_btn.opacity = 1
            if self.story_engine and not self.story_engine.has_next():
                self.next_btn.text = "Finish"
                self.next_btn.disabled = False
            else:
                self.next_btn.text = "Seguir"
                self.next_btn.disabled = not self.story_engine.has_next()
        self.prev_btn.disabled = not self.story_engine.has_previous()

    def start_minigame(self, screen_name):
        self.manager.on_minigame_complete = self.on_minigame_complete
        self.manager.last_screen = "story"
        self.manager.current = screen_name

    def on_minigame_complete(self):
        if self.story_engine and self.story_engine.has_next():
            self.story_engine.next_page()
            self.show_page(self.story_engine.current_index)
            self.manager.current = "story"
        else:
            self.manager.current = "end"

    def go_next(self, instance):
        if self.story_engine and not self.story_engine.has_next():
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
