from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty
import os

class DrawingCanvas(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(255, 255, 255)
                touch.ud["line"] = Line(points=[touch.x, touch.y], width=2)

    def on_touch_move(self, touch):
        if "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]

    def save_to_file(self, filename="drawing_output.png"):
        # Construct full path inside the sacred folder
        full_path = os.path.join("assets", "images", filename)
        self.export_to_png(full_path)
        return full_path


class DrawingGameScreen(Screen):
    canvas_area = ObjectProperty(None)
    
    def on_pre_enter(self):
        self.canvas_area.canvas.clear()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="Draw something!", font_size=28))

        self.canvas_area = DrawingCanvas()
        layout.add_widget(self.canvas_area)

        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=20)
        complete_btn = Button(text="Complete Drawing", font_size=22)
        complete_btn.bind(on_release=self.complete_game)
        clear_btn = Button(text="Clear", font_size=22)
        clear_btn.bind(on_release=lambda x: self.canvas_area.canvas.clear())

        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(complete_btn)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def complete_game(self, instance):
        filename = self.canvas_area.save_to_file()
        print(f"✅ Drawing saved to {filename}")

        if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
            self.manager.challenge_mode = False
            self.manager.current = "challenge_selection"
        elif hasattr(self.manager, "on_minigame_complete"):
            self.manager.on_minigame_complete()
        else:
            self.manager.current = "story"
