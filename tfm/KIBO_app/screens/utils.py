from kivy.uix.button import Button

def make_back_button(callback):
    back_btn = Button(text="Back", size_hint=(None, None), size=(120, 50), font_size=18, pos_hint={'x': 0, 'top': 1})
    back_btn.bind(on_release=callback)
    return back_btn