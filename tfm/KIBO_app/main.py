import os
from kivy.config import Config
def is_raspberry_pi():
    try:
        with open("/proc/device-tree/model") as f:
            model = f.read().lower()
        return "raspberry pi" in model
    except Exception:
        return False

on_pi = is_raspberry_pi()

if on_pi:
    os.environ['KIVY_BCM_DISPMANX_ID'] = '2'
    Config.set('graphics', 'fullscreen', '1')
    Config.set('graphics', 'borderless', '1')
    Config.set('graphics', 'show_cursor', '0')
else:
    # macOS or dev machine: windowed mode
    Config.set('graphics', 'fullscreen', '0')
    Config.set('graphics', 'width', '480')
    Config.set('graphics', 'height', '800')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.text import LabelBase
from kivy.lang import Builder

from screens.splash import SplashScreen
from screens.home import HomeScreen
from screens.level_selection import LevelSelectionScreen
from screens.story import StoryScreen
from screens.end import EndScreen
from screens.challenge_selection import ChallengeSelectionScreen
from screens.switch import SwitchScreen

from minigames.drawing_game import DrawingGameScreen
from minigames.memory_game import MemoryGameScreen
from minigames.lost_and_found import LostAndFoundScreen
from minigames.potentiometer_game import PotentiometerGameScreen
from minigames.color_choice import ColorChoiceScreen
from minigames.multiple_choice import MultipleChoiceScreen

# Absolute path logic
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.normpath(os.path.join(current_dir, 'assets', 'fonts', 'KGNeatlyPrintedSpaced.ttf'))

LabelBase.register(name='MyFont', fn_regular=font_path)

kv_path = os.path.join(os.path.dirname(__file__), 'style.kv')
Builder.load_file(kv_path)

class SacredScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
    #pass

class SacredApp(App):
    def build(self):
        sm = SacredScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LevelSelectionScreen(name="level_selection"))
        sm.add_widget(StoryScreen(name="story"))
        sm.add_widget(EndScreen(name="end"))
        sm.add_widget(ChallengeSelectionScreen(name="challenge_selection"))
        sm.add_widget(DrawingGameScreen(name="drawing_game"))
        sm.add_widget(MemoryGameScreen(name="memory_game"))
        sm.add_widget(LostAndFoundScreen(name="lost_and_found"))
        sm.add_widget(PotentiometerGameScreen(name="potentiometer_game"))
        sm.add_widget(ColorChoiceScreen(name="color_choice"))
        sm.add_widget(MultipleChoiceScreen(name="multiple_choice"))
        sm.add_widget(SwitchScreen(name="switch"))
        sm.current = "splash" # set to splash to start regular, DEBUG SCREEN by placing it here
        return sm

if __name__ == "__main__":
    SacredApp().run()
