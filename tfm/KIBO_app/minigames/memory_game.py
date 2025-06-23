from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from core.image_manager import ImageManager
from core.utils import fade_in, fade_out, make_back_button
from core.serial_manager import SerialManager

class MemoryGameScreen(Screen):
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
        # Serial: send command and bind listeners for win/lose
        SerialManager.get_instance().send("MEM")
        SerialManager.get_instance().bind_message("win", self.on_serial_win)
        SerialManager.get_instance().bind_message("lose", self.on_serial_lose)

    def on_leave(self):
        SerialManager.get_instance().unbind_message("win")
        SerialManager.get_instance().unbind_message("lose")

    def on_serial_win(self):
        from core.audio_manager import AudioManager
        AudioManager.get_instance().play_sound_effect("win")
        print("Serial: win received in memory game")
        self.go_back(None)

    def on_serial_lose(self):
        from core.audio_manager import AudioManager
        AudioManager.get_instance().play_sound_effect("lose")
        SerialManager.get_instance().send("MEM")
        print("Serial: lose received in memory game")

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
            text="¡Mira el patrón de luces en los botones de la izquierda, recuérdalo y luego ingrésalo nuevamente para continuar!",
            font_size=98,
            color=(1,1,1,1),
            size_hint=(0.8, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            halign="center",
            valign="top",
            text_size=(0, None)
        )
        def update_label_height(instance, value):
            instance.text_size = (instance.width, None)
            instance.texture_update()
            instance.height = instance.texture_size[1]
        label.bind(width=update_label_height, text=update_label_height)
        update_label_height(label, None)
        self.ui_layout.add_widget(label)

        # No complete button; game completion is handled by on_serial_win()

    def go_back(self, instance):
        SerialManager.get_instance().send("i")
        def switch_screen():
            last = getattr(self.manager, "last_screen", None)
            if last == "story":
                self.manager.current = "story"
            else:
                self.manager.current = "challenge_selection"
        fade_out(self.ui_layout, on_complete=switch_screen)
