from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from core.video_manager import VideoManager
from core.image_manager import ImageManager

class SwitchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.video_manager = VideoManager(self.layout)
        self.from_screen = None
        self.to_screen = None
        self.subject = None
        self.background_widget = None

    def on_enter(self):
        self.from_screen = self.manager.last_screen
        self.to_screen = self.manager.next_screen
        self.subject = getattr(self.manager, "next_subject", None)

        if not self.from_screen or not self.to_screen:
            print("❌ Missing 'last_screen' or 'next_screen' in ScreenManager")
            return

        self.start_transition()

    def start_transition(self):
        print(f"🔄 Switching from {self.from_screen} to {self.to_screen}")

        # Determine background for FROM screen
        if self.from_screen == "level_selection" and self.subject:
            bg_name = self.subject
        else:
            bg_name = self.from_screen

        self.background_widget = ImageManager.get_image_widget(bg_name, allow_stretch=True, keep_ratio=False)
        if self.background_widget:
            self.layout.add_widget(self.background_widget, index=0)

        Clock.schedule_once(self.play_transition_video, 0.1)

    def play_transition_video(self, dt):
        if self.from_screen == "home" and self.to_screen == "level_selection" and self.subject:
            video_name = f"{self.from_screen}TO{self.subject}"
        elif self.from_screen == "level_selection" and self.to_screen == "home" and self.subject:
            video_name = f"{self.subject}TO{self.to_screen}"
        else:
            video_name = f"{self.from_screen}TO{self.to_screen}"

        print(f"🎬 Playing transition video: {video_name}.mp4")
        self.video_manager.play_video(
            video_name,
            on_finish=self.after_video,
            background_widget=self.background_widget
        )

    def after_video(self):
        print(f"🎯 Transition video complete. Loading {self.to_screen} background.")
        self.layout.clear_widgets()

        # Determine background for TO screen
        if self.to_screen == "level_selection" and self.subject:
            bg_name = self.subject
        else:
            bg_name = self.to_screen

        new_bg = ImageManager.get_image_widget(bg_name, allow_stretch=True, keep_ratio=False)
        if new_bg:
            self.layout.add_widget(new_bg, index=0)

        Clock.schedule_once(self.finish_transition, 0.1)

    def finish_transition(self, dt):
        print(f"✅ Switch complete. Entering {self.to_screen}")
        self.manager.last_screen = "switch"
        self.manager.current = self.to_screen
