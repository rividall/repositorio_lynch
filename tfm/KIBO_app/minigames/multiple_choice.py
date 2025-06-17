
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.question_loader import QuestionLoader
from core.audio_manager import AudioManager

class MultipleChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.question_label = Label(text="Loading question...", font_size=28)
        self.layout.add_widget(self.question_label)

        self.button_layout = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)
        self.load_new_question()

    def on_pre_enter(self):
        self.load_new_question()

    def load_new_question(self):
        loader = QuestionLoader("math", 1, base_path="assets/questions")
        self.current_question = loader.get_random_question()

        self.question_label.text = self.current_question["question"]
        correct_answer = self.current_question["correct_answer"]
        options = self.current_question["options"]

        # Select 3 wrong + 1 correct answer
        wrong = [opt for opt in options if opt != correct_answer]
        choices = [correct_answer] + random.sample(wrong, 3)
        random.shuffle(choices)

        self.button_layout.clear_widgets()
        for choice in choices:
            btn = Button(text=choice, font_size=24, size_hint_y=None, height=60)
            btn.bind(on_release=self.check_answer)
            self.button_layout.add_widget(btn)

    def check_answer(self, instance):
        selected = instance.text
        correct = self.current_question["correct_answer"]
        print("✅ Correct!" if selected == correct else "❌ Incorrect!")
        if selected == correct : 
            AudioManager.get_instance().play_sound_effect("correct")
        else:
            AudioManager.get_instance().play_sound_effect("error")
        # Notify game complete
        if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
            self.manager.challenge_mode = False
            self.manager.current = "challenge_selection"
        elif hasattr(self.manager, "on_minigame_complete"):
            self.manager.on_minigame_complete()
        else:
            self.manager.current = "story"
