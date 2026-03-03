from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from core.utils import fade_in, fade_out, home_button, make_back_button
from core.question_loader import QuestionLoader
from core.audio_manager import AudioManager
from core.serial_manager import SerialManager
from core.image_manager import ImageManager
import random

class MultipleChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

        self.bg = None
        self.question_label = None
        self.answer_buttons = []
        self.current_question = None

    def on_enter(self):
        self.bg = ImageManager.get_image_widget("desafio1", allow_stretch=True, keep_ratio=False)
        self.bg_layout.clear_widgets()
        if self.bg:
            self.bg_layout.add_widget(self.bg)

        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)

        # Serial: send command and bind listeners
        SerialManager.get_instance().send("MULT")
        self._bind_serial_buttons()

    def _bind_serial_buttons(self):
        sm = SerialManager.get_instance()
        sm.unbind_all()
        sm.bind_message("btn1", lambda: self._on_serial_btn(0))
        sm.bind_message("btn2", lambda: self._on_serial_btn(1))
        sm.bind_message("btn3", lambda: self._on_serial_btn(2))
        sm.bind_message("btn4", lambda: self._on_serial_btn(3))

    def _on_serial_btn(self, idx):
        # Only allow one answer per question
        sm = SerialManager.get_instance()
        sm.unbind_all()
        self.check_answer_by_index(idx)

    def on_leave(self):
        SerialManager.get_instance().unbind_all()

    def build_ui(self):
        self.ui_layout.clear_widgets()

        root = FloatLayout()

        # Back button
        back_btn = make_back_button(self.go_back)
        self.ui_layout.add_widget(back_btn)

        self.question_label = Label(
            text="Loading question...",
            font_size=90,
            color=(1,1,1,1),
            size_hint=(0.8, 0.5),
            pos_hint={'x': 0.1, 'y': 0.5},
            halign="center",
            valign="middle",
            text_size=(self.width * 0.9, self.height * 0.7)
        )
        def update_text_size(instance, value):
            instance.text_size = (instance.width, instance.height)
        self.question_label.bind(size=update_text_size)
        root.add_widget(self.question_label)

        # Colored rounded square buttons in a 2x2 grid
        button_colors = [
            (0.6, 0.2, 0.6, 1),   # Purple
            (1, 0.2, 0.2, 1),     # Red
            (0.2, 0.8, 0.8, 1),   # Turquoise
            (1, 0.8, 0.1, 1),         # Yellow
        ]

        grid_container = FloatLayout(
            size_hint=(0.8, 0.5),
            pos_hint={'x': 0.1, 'y': 0.05}
        )
        grid = GridLayout(
            cols=2,
            rows=2,
            spacing=20,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        self.answer_buttons = []
        for i in range(4):
            color = button_colors[i]
            btn = Button(
                text="",
                color=(1,1,1,1),
                disabled_color=(1,1,1,1),
                font_size=172,
                background_normal='',
                background_color=(0, 0, 0, 0),
                size_hint=(1, 1)
            )
            btn.disabled = True
            with btn.canvas.before:
                Color(*color)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[30])
                btn.bind(pos=lambda instance, value, r=btn.rect: setattr(r, 'pos', value))
                btn.bind(size=lambda instance, value, r=btn.rect: setattr(r, 'size', value))
            self.answer_buttons.append(btn)
            grid.add_widget(btn)

        grid_container.add_widget(grid)
        root.add_widget(grid_container)
        self.ui_layout.add_widget(root)
        self.load_new_question()

    def load_new_question(self):
        loader = QuestionLoader("math", 1, base_path="assets/questions")
        self.current_question = loader.get_random_question()

        self.question_label.text = self.current_question["question"]
        correct_answer = self.current_question["correct_answer"]
        options = self.current_question["options"]

        wrong = [opt for opt in options if opt != correct_answer]
        choices = [correct_answer] + random.sample(wrong, 3)
        random.shuffle(choices)

        for i, btn in enumerate(self.answer_buttons):
            btn.text = choices[i]

        # Re-bind serial buttons for the new question
        self._bind_serial_buttons()

    def check_answer_by_index(self, index):
        if index < len(self.answer_buttons):
            self.check_answer(self.answer_buttons[index])

    def check_answer(self, button):
        selected = button.text
        correct = self.current_question["correct_answer"]
        print("✅ Correct!" if selected == correct else "❌ Incorrect!")
        if selected == correct:
            AudioManager.get_instance().play_sound_effect("correct")
        else:
            AudioManager.get_instance().play_sound_effect("error")
            # Load a new question on incorrect answer and return
            self.load_new_question()
            SerialManager.get_instance().send("MULT")
            return

        if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
            self.manager.challenge_mode = False
            fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "challenge_selection"))
        elif hasattr(self.manager, "on_minigame_complete"):
            self.manager.on_minigame_complete()
        else:
            fade_out(self.ui_layout, on_complete=lambda: setattr(self.manager, "current", "story"))

    def go_back(self, instance):
        SerialManager.get_instance().send("i")
        def switch_screen():
            last = getattr(self.manager, "last_screen", None)
            if last == "story":
                self.manager.current = "story"
            else:
                self.manager.current = "challenge_selection"
        fade_out(self.ui_layout, on_complete=switch_screen)
