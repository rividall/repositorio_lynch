# core/audio_manager.py - Audio playback using VLC
import os
import vlc

class AudioManager:
    _instance = None

    def __init__(self):
        self.player = None
        self.started = False

    def start_background_music(self):
        if not self.started:
            path = os.path.join("assets", "audio", "background.mp3")
            self.player = vlc.MediaPlayer(path)
            self.player.audio_set_volume(100)
            self.player.play()
            self.started = True

    def loop_music(self):
        if self.player and self.player.get_state() == vlc.State.Ended:
            self.player.stop()
            self.player.play()

    def play_sound_effect(self, sound_name):
        """Play a named sound effect, mapped internally to a file name."""
        sound_map = {
            "correct": "correct.mp3",
            "error": "error.mp3",
            "click": "click.mp3",
            "win": "win.mp3",
            "lose": "lose.mp3"
        }

        filename = sound_map.get(sound_name)
        if not filename:
            print(f"⚠️ Unknown sound effect: '{sound_name}'")
            return

        effect_path = os.path.join("assets", "audio", filename)
        if os.path.exists(effect_path):
            p = vlc.MediaPlayer(effect_path)
            p.audio_set_volume(80)
            p.play()
            print(f"Sound effect played: {effect_path}")
        else:
            print(f"⚠️ Sound effect file not found: {effect_path}")


    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = AudioManager()
        return cls._instance

