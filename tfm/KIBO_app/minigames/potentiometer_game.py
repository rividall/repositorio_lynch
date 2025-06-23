from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.image_manager import ImageManager
from core.utils import fade_in, fade_out, make_back_button
from core.serial_manager import SerialManager

class PotentiometerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_layout = FloatLayout()
        self.ui_layout = FloatLayout()
        self.add_widget(self.bg_layout)
        self.add_widget(self.ui_layout)

    def on_enter(self):
        self.bg_layout.clear_widgets()
        self.ui_layout.clear_widgets()
        self.load_background()
        self.build_ui()
        fade_in(self.ui_layout)
        fade_in(self.bg_layout)
        # Serial: send command and bind listeners for potentiometer values
        SerialManager.get_instance().send("POTE")
        SerialManager.get_instance().bind_message("0", lambda: self.on_serial_potval(0))
        SerialManager.get_instance().bind_message("1", lambda: self.on_serial_potval(1))
        SerialManager.get_instance().bind_message("potVal", self.on_serial_potval)
        self.potval_label = None  # Will be set in build_ui

    def on_leave(self):
        SerialManager.get_instance().unbind_message("0")
        SerialManager.get_instance().unbind_message("1")
        SerialManager.get_instance().unbind_message("potVal")

    def on_serial_potval(self, value=None):
        # value is now always 0 or 1 for "0" and "1" messages
        if value is None:
            val = "?"
        else:
            val = value
        if hasattr(self, "potval_label") and self.potval_label:
            self.potval_label.text = f"potVal: {val}"
        print(f"Serial: potVal received in potentiometer game: {val}")

    def load_background(self):
        bg = ImageManager.get_image_widget("desafio4", allow_stretch=True, keep_ratio=False)
        if bg:
            self.bg_layout.add_widget(bg)

    def build_ui(self):
        # Back button (top left)
        back_btn = make_back_button(self.go_back)
        self.ui_layout.add_widget(back_btn)

        # Centered label with instructions
        label = Label(
            text="Potentiometer Game (placeholder)",
            font_size=28,
            color=(1,1,1,1),
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            halign="center",
            valign="middle"
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
        self.ui_layout.add_widget(label)

        # Label to display potVal
        self.potval_label = Label(
            text="potVal: ?",
            font_size=24,
            color=(1,1,0,1),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            halign="center",
            valign="middle"
        )
        self.potval_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
        self.ui_layout.add_widget(self.potval_label)

        # Complete button
        complete_btn = Button(
            text="Complete Potentiometer Game",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            font_size=22
        )
        complete_btn.bind(on_release=self.complete_game)
        self.ui_layout.add_widget(complete_btn)

    def go_back(self, instance):
        SerialManager.get_instance().send("i")
        def switch_screen():
            last = getattr(self.manager, "last_screen", None)
            if last == "story":
                self.manager.current = "story"
            else:
                self.manager.current = "challenge_selection"
        fade_out(self.ui_layout, on_complete=switch_screen)

    def complete_game(self, instance):
        def switch_screen():
            if hasattr(self.manager, "challenge_mode") and self.manager.challenge_mode:
                self.manager.challenge_mode = False
                self.manager.current = "challenge_selection"
            elif hasattr(self.manager, "on_minigame_complete"):
                self.manager.on_minigame_complete()
            else:
                self.manager.current = "story"
        fade_out(self.ui_layout, on_complete=switch_screen)