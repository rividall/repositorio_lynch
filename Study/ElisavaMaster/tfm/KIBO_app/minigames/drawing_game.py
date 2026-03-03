from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty
from kivy.graphics import Fbo, Color, Line, ClearColor, ClearBuffers, PushMatrix, PopMatrix, Scale, Translate
from kivy.core.image import Image as CoreImage
from PIL import Image as PILImage
from core.utils import fade_in, fade_out
import os
import io

class DrawingCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strokes = []  # Store all strokes as list of (Color, Line)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                color = Color(0, 0, 0, 1)
                line = Line(points=[touch.x, touch.y], width=2)
                self.strokes.append((color.rgba, [touch.x, touch.y]))  # store color + stroke

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            for stroke in self.strokes[-1:]:
                stroke[1].extend([touch.x, touch.y])
            for instr in self.canvas.children:
                if isinstance(instr, Line):
                    instr.points += [touch.x, touch.y]

    def save_to_file(self, filename="drawing_output.png"):
        full_path = os.path.join("assets", "images", filename)

        # Create transparent FBO
        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 0)  # Fully transparent
            ClearBuffers()
            PushMatrix()
            Scale(1, -1, 1)  # Flip Y axis
            Translate(-self.x, -self.y - self.height, 0)

            # Re-draw strokes from memory
            for color_rgba, points in self.strokes:
                Color(*color_rgba)
                Line(points=points, width=2)

            PopMatrix()

        fbo.draw()

        # Convert Fbo texture to RGBA byte buffer
        data = fbo.texture.pixels
        size = fbo.size

        # Create a PIL image and save with true transparency
        image = PILImage.frombytes('RGBA', (int(size[0]), int(size[1])), data)
        image = image.transpose(PILImage.FLIP_TOP_BOTTOM)  # Important!
        image.save(full_path)

        return full_path


class DrawingGameScreen(Screen):
    canvas_area = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)
        self.canvas_area = None

    def on_pre_enter(self):
        if self.canvas_area:
            self.canvas_area.canvas.clear()
        self.bg_layout.clear_widgets()
        self.ui_layout.clear_widgets()
        self.load_background()
        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)

    def load_background(self):
        bg = Image(source="assets/images/matemáticas_story.png", allow_stretch=True, keep_ratio=False)
        self.bg_layout.add_widget(bg)

    def build_ui(self):
        from core.utils import make_back_button
        # Back button (top left)
        back_btn = make_back_button(self.go_back)
        self.ui_layout.add_widget(back_btn)

        # Label at the top
        label = Label(
            text="Draw something!",
            font_size=32,
            color=(1,1,1,1),
            size_hint=(0.9, 0.15),
            pos_hint={'center_x': 0.5, 'top': 0.98},
            halign="center",
            valign="top"
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
        self.ui_layout.add_widget(label)

        # Drawing canvas in the center, from x0.1 y0.1 to x0.9 y0.9
        self.canvas_area = DrawingCanvas(
            size_hint=(0.8, 0.8),
            pos_hint={'x': 0.1, 'y': 0.1}
        )
        self.ui_layout.add_widget(self.canvas_area)

        # Buttons below the canvas, overlayed at the bottom
        from core.utils import home_button
        btn_layout = BoxLayout(
            size_hint=(0.5, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            spacing=20
        )
        clear_btn = home_button(
            "matemáticasbtn",
            0, 0, 220, 80,
            "Borrar",
            lambda x: self.canvas_area.canvas.clear()
        )
        complete_btn = home_button(
            "desafiobtn",
            0, 0, 260, 80,
            "Listo",
            self.complete_game
        )
        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(complete_btn)
        self.ui_layout.add_widget(btn_layout)

    def go_back(self, instance):
        def switch_screen():
            last = getattr(self.manager, "last_screen", None)
            if last == "story":
                self.manager.current = "story"
            else:
                self.manager.current = "challenge_selection"
        fade_out(self.ui_layout, on_complete=switch_screen)

    def complete_game(self, instance):
        filename = self.canvas_area.save_to_file()
        print(f"✅ Drawing saved to {filename}")

        def switch_screen():
            if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
                self.manager.challenge_mode = False
                self.manager.current = "challenge_selection"
            elif hasattr(self.manager, "on_minigame_complete"):
                self.manager.on_minigame_complete()
            else:
                self.manager.current = "story"
        fade_out(self.ui_layout, on_complete=switch_screen)
