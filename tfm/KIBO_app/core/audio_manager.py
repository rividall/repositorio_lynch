# core/audio_manager.py
import os
import vlc
import threading
import time

class AudioManager:
    _instance = None

    def __init__(self):
        self.player = None
        self.started = False
        self.current_track = None

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_audio_path = os.path.normpath(os.path.join(current_dir, "..", "assets", "audio"))

    def start_background_music(self):
        self.change_background_music("background")

    def loop_music(self):
        if self.player and self.player.get_state() == vlc.State.Ended:
            self.player.stop()
            self.player.play()

    def change_background_music(self, song_name):
        """
        Fade out current track, then fade in the new track (by name, without extension).
        """
        filename = f"{song_name}.mp3"
        path = os.path.abspath(os.path.join(self.base_audio_path, filename))

        if not os.path.exists(path):
            print(f"⚠️ Requested music file not found: {path}")
            return

        if self.current_track == path and self.player and self.player.get_state() == vlc.State.Playing:
            return  # Already playing this

        def _start_new_track():
            self.player = vlc.MediaPlayer(path)
            self.player.audio_set_volume(0)
            self.player.play()
            self.current_track = path
            self.started = True
            self._fade_in_new_track()
            print(f"🎶 Now playing with fade-in: {filename}")

        # If there's music playing, fade it out first
        if self.player and self.player.get_state() == vlc.State.Playing:
            self._fade_out_current_track(on_complete=_start_new_track)
        else:
            _start_new_track()

    def _fade_out_current_track(self, on_complete=None, duration=1.5):
        """
        Gradually lowers the volume and stops the player.
        """
        def fade():
            steps = 10
            interval = duration / steps
            for i in range(steps):
                vol = max(0, 100 - int((i + 1) * (100 / steps)))
                if self.player:
                    self.player.audio_set_volume(vol)
                time.sleep(interval)
            if self.player:
                self.player.stop()
            if on_complete:
                on_complete()

        threading.Thread(target=fade, daemon=True).start()

    def _fade_in_new_track(self, duration=1.5):
        """
        Gradually raises the volume on the new track.
        """
        def fade():
            steps = 10
            interval = duration / steps
            for i in range(steps):
                vol = min(100, int((i + 1) * (100 / steps)))
                if self.player:
                    self.player.audio_set_volume(vol)
                time.sleep(interval)

        threading.Thread(target=fade, daemon=True).start()

    def play_sound_effect(self, sound_name):
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

        effect_path = os.path.abspath(os.path.join(self.base_audio_path, filename))
        if os.path.exists(effect_path):
            p = vlc.MediaPlayer(effect_path)
            p.audio_set_volume(80)
            p.play()
            print(f"🎵 Sound effect played: {effect_path}")
        else:
            print(f"⚠️ Sound effect file not found: {effect_path}")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = AudioManager()
        return cls._instance
