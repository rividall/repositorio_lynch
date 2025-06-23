import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from core.question_loader import QuestionLoader
from core.audio_manager import AudioManager
from core.serial_manager import SerialManager
from core.utils import make_back_button

class MultipleChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serial = SerialManager.get_instance()

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.top_bar = BoxLayout(size_hint=(1, None), height=60)
        self.top_bar.add_widget(make_back_button(self.go_back))
        self.top_bar.add_widget(Label(size_hint=(1, 1)))
        self.layout.add_widget(self.top_bar)

        self.question_label = Label(text="Loading question...", font_size=28)
        self.layout.add_widget(self.question_label)

        self.answer_labels = []
        self.answer_box = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.answer_box)

        self.status = Label(text="", font_size=20)
        self.layout.add_widget(self.status)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_new_question()

    def on_enter(self):
        self.serial.bind_message("btn1", lambda: self.check_answer(0))
        self.serial.bind_message("btn2", lambda: self.check_answer(1))
        self.serial.bind_message("btn3", lambda: self.check_answer(2))
        self.serial.bind_message("btn4", lambda: self.check_answer(3))

    def on_leave(self):
        self.serial.unbind_all()

    def load_new_question(self):
        loader = QuestionLoader("math", 1, base_path="assets/questions")
        self.current_question = loader.get_random_question()

        self.question_label.text = self.current_question["question"]
        correct_answer = self.current_question["correct_answer"]
        options = self.current_question["options"]

        wrong = [opt for opt in options if opt != correct_answer]
        self.choices = [correct_answer] + random.sample(wrong, 3)
        random.shuffle(self.choices)

        self.answer_box.clear_widgets()
        self.answer_labels = []
        for i, choice in enumerate(self.choices):
            label = Label(text=f"{i+1}. {choice}", font_size=24)
            self.answer_labels.append(label)
            self.answer_box.add_widget(label)

        self.status.text = ""

    def check_answer(self, index):
        selected = self.choices[index]
        correct = self.current_question["correct_answer"]
        print("✅ Correct!" if selected == correct else "❌ Incorrect!")

        if selected == correct:
            AudioManager.get_instance().play_sound_effect("correct")
        else:
            AudioManager.get_instance().play_sound_effect("error")

        self.status.text = "¡Correcto! 🎉" if selected == correct else "❌ Incorrecto. Intenta de nuevo."

        if selected == correct:
            if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
                self.manager.challenge_mode = False
                self.manager.current = "challenge_selection"
            elif hasattr(self.manager, "on_minigame_complete"):
                self.manager.on_minigame_complete()
            else:
                self.manager.current = "story"

    def go_back(self, instance):
        self.manager.last_screen = "multiple_choice"
        self.manager.next_screen = "home"
        self.manager.current = "switch"
