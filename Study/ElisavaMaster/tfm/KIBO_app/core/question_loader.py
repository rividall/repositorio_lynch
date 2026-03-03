import json
import os
import random

class QuestionLoader:
    def __init__(self, subject: str, level: int, base_path="assets/questions"):
        self.subject = subject
        self.level = level
        self.base_path = base_path
        self.questions = self.load_questions()

    def load_questions(self):
        filename = f"{self.subject}_questions{self.level}.json"
        # Always resolve path from the script's folder
        root = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(root, "..", self.base_path, filename)
        filepath = os.path.normpath(filepath)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Question file not found: {filepath}")

        with open(filepath, "r") as f:
            data = json.load(f)
        return data.get("questions", [])

    def get_random_question(self):
        if not self.questions:
            raise ValueError("No questions available")
        return random.choice(self.questions)