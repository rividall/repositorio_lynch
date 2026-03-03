from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from core.utils import fade_in, fade_out, make_back_button
from core.serial_manager import SerialManager
from core.audio_manager import AudioManager

# Colors for lighting up
RECT_COLORS = [
    (1, 0, 1, 1),    # btn1 - Red
    (1, 0, 0, 1),    # btn2 - Green
    (1, 1, 0, 1),    # btn3 - Blue
    (1, 1, 0, 1),    # btn4 - Yellow
]
GREY = (0.5, 0.5, 0.5, 1)

# Sound effect names for each button (place files in assets/audio/)
RECT_SOUNDS = [
    "color_btn1",  # btn1 - top left
    "color_btn2",  # btn2 - top right
    "color_btn3",  # btn3 - bottom left
    "color_btn4",  # btn4 - bottom right
]

class ColorRect(Widget):
    def __init__(self, color=GREY, **kwargs):
        super().__init__(**kwargs)
        self.current_color = color
        with self.canvas:
            self.color_instr = Color(*self.current_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[30])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def set_color(self, color):
        self.current_color = color
        self.color_instr.rgba = color

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ColorChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)
        self.rects = []

    def on_enter(self):
        self.bg_layout.clear_widgets()
        self.ui_layout.clear_widgets()
        # Add background image "desafio1"
        from core.image_manager import ImageManager
        bg = ImageManager.get_image_widget("desafio1", allow_stretch=True, keep_ratio=False)
        if bg:
            self.bg_layout.add_widget(bg)
        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)
        self._bind_serial_buttons()

    def on_leave(self):
        self._unbind_serial_buttons()

    def build_ui(self):
        # Back button (optional, top left)
        back_btn = make_back_button(self.go_back)
        self.ui_layout.add_widget(back_btn)

        # 2x2 grid for rectangles, lower half of the screen
        grid = GridLayout(
            cols=2,
            rows=2,
            spacing=20,
            size_hint=(0.8, 0.4),
            pos_hint={'x': 0.1, 'y': 0.05}
        )
        self.rects = []
        for i in range(4):
            rect = ColorRect()
            self.rects.append(rect)
            grid.add_widget(rect)
        self.ui_layout.add_widget(grid)

    def _bind_serial_buttons(self):
        SerialManager.get_instance().send("MIDI")
        sm = SerialManager.get_instance()
        sm.unbind_all()
        sm.bind_message("btn1", lambda: self._on_btn(0))
        sm.bind_message("btn2", lambda: self._on_btn(1))
        sm.bind_message("btn3", lambda: self._on_btn(2))
        sm.bind_message("btn4", lambda: self._on_btn(3))
        sm.bind_message("EOG", self._on_eog)

    def _unbind_serial_buttons(self):
        sm = SerialManager.get_instance()
        sm.unbind_all()

    def _on_btn(self, idx):
        # Light up the corresponding rectangle
        for i, rect in enumerate(self.rects):
            rect.set_color(GREY)
        if 0 <= idx < len(self.rects):
            self.rects[idx].set_color(RECT_COLORS[idx])
            # Play unique sound effect for each button
            sound_name = RECT_SOUNDS[idx] if idx < len(RECT_SOUNDS) else "click"
            print(sound_name)
            AudioManager.get_instance().play_sound_effect(sound_name)
            # Schedule to revert to grey after 200ms
            Clock.schedule_once(lambda dt, i=idx: self.rects[i].set_color(GREY), 0.2)

    def _on_eog(self, *args, **kwargs):
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "challenge_selection"))

    def go_back(self, instance):
        SerialManager.get_instance().send("i")
        fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "challenge_selection"))