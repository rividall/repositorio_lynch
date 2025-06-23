from kivy.uix.button import Button
from kivy.animation import Animation
import os
from core.audio_manager import AudioManager

def make_back_button(callback):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.normpath(os.path.join(current_dir, "..", "assets", "images", "backArrow.png"))

    def on_press_sound(instance):
        AudioManager.get_instance().play_sound_effect("click")
        callback(instance)

    back_btn = Button(
        size_hint=(None, None),
        size=(140, 110),  # Adjust if needed
        pos_hint={'x': 0.02, 'top': 0.98},  # ✅ Valid top-left positioning
        background_normal=img_path,
        background_down=img_path,
        border=(0, 0, 0, 0),
        text='',  # ✅ Image only
        background_color=(1, 1, 1, 1)
    )
    back_btn.bind(on_release=on_press_sound)
    return back_btn

def make_forward_button(callback):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.normpath(os.path.join(current_dir, "..", "assets", "images", "fwdArrow.png"))

    def on_press_sound(instance):
        AudioManager.get_instance().play_sound_effect("click")
        callback(instance)

    fwd_btn = Button(
        size_hint=(None, None),
        size=(170, 140),  # Adjust if needed
        pos_hint={'right': 0.98, 'y': 0.02},  # ✅ Bottom-right corner
        background_normal=img_path,
        background_down=img_path,
        border=(0, 0, 0, 0),
        text='',  # ✅ Image only
        background_color=(1, 1, 1, 1)
    )
    fwd_btn.bind(on_release=on_press_sound)
    return fwd_btn

def home_button(img_name, x, y, width, height, callback):
    # Absolute path for image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.normpath(os.path.join(current_dir, "..", "assets", "images", img_name + ".png"))

    def on_press_sound(instance):
        AudioManager.get_instance().play_sound_effect("click")
        callback(instance)

    btn = Button(
        size_hint=(None, None),
        size=(width, height),
        pos_hint={'x': x, 'y': y},
        background_normal=img_path,
        background_down=img_path,
        border=(0, 0, 0, 0),
        background_color=(1, 1, 1, 1),
        text=""
    )
    btn.bind(on_release=on_press_sound)
    return btn

from kivy.animation import Animation

def fade_out(layout, duration=0.3, on_complete=None):
    """
    Fades out all children of the given layout.
    """
    children = layout.children[:]
    for i, widget in enumerate(children):
        anim = Animation(opacity=0, duration=duration)
        if on_complete and i == 0:  # Only bind once
            anim.bind(on_complete=lambda *_: on_complete())
        anim.start(widget)

def fade_in(layout, duration=0.3):
    """
    Fades in all children of the given layout.
    """
    for widget in layout.children:
        widget.opacity = 0  # Ensure starts invisible
        Animation(opacity=1, duration=duration).start(widget)