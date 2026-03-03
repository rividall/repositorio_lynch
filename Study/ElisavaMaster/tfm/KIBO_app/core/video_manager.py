import os
from kivy.uix.video import Video
from kivy.clock import Clock

class VideoManager:
    _preloaded_videos = {}

    def __init__(self, parent_layout):
        self.parent_layout = parent_layout
        self.video_widget = None

    @classmethod
    def preload_video(cls, video_name):
        if video_name in cls._preloaded_videos:
            return  # Already preloaded

        filename = f"{video_name}.mp4"
        if not filename:
            #print(f"⚠️ Unknown video to preload: '{video_name}'")
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_dir = os.path.normpath(os.path.join(current_dir, "..", "assets", "video"))
        path = os.path.join(video_dir, filename)

        if not os.path.exists(path):
            #print(f"⚠️ Video file not found for preload: {path}")
            return

        #print(f"📦 Preloading video: {video_name} from {path}")
        video = Video(source=path, state='stop', volume=0)
        video.allow_stretch = True
        video.keep_ratio = False
        video.options = {'eos': 'stop'}
        video.opacity = 0

        cls._preloaded_videos[video_name] = video

    def play_video(self, video_name, on_finish=None, loop=False, use_preloaded=True, background_widget=None):
        def reveal_and_remove_bg(video_widget):
            def reveal_video(*args):
                def delayed_show(dt):
                    video_widget.opacity = 1
                    if background_widget and background_widget.parent:
                        self.parent_layout.remove_widget(background_widget)
                Clock.schedule_once(delayed_show, 0.1)
            video_widget.bind(texture=reveal_video)


        filename = f"{video_name}.mp4"
        if not filename:
            #print(f"⚠️ Unknown video: '{video_name}'")
            if on_finish:
                on_finish()
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_dir = os.path.normpath(os.path.join(current_dir, "..", "assets", "video"))
        path = os.path.join(video_dir, filename)

        if not os.path.exists(path):
            #print(f"⚠️ Video file not found: {path}")
            if on_finish:
                on_finish()
            return

        if self.video_widget:
            self.parent_layout.remove_widget(self.video_widget)

        # Load preloaded or create new
        if use_preloaded and video_name in self._preloaded_videos:
            self.video_widget = self._preloaded_videos[video_name]
            self.video_widget.state = 'play'
            self.video_widget.options = {'eos': 'loop' if loop else 'stop'}
            # ⚠ Ensure no duplicate parenting
            if self.video_widget.parent:
                self.video_widget.parent.remove_widget(self.video_widget)
        else:
            self.video_widget = Video(source=path, state='play', volume=0)
            self.video_widget.allow_stretch = True
            self.video_widget.keep_ratio = False
            self.video_widget.options = {'eos': 'loop' if loop else 'stop'}
            self.video_widget.opacity = 0

        self.parent_layout.add_widget(self.video_widget)
        reveal_and_remove_bg(self.video_widget)

        if not loop:
            def check_finished(dt):
                if self.video_widget and self.video_widget.state == 'stop':
                    self.parent_layout.remove_widget(self.video_widget)
                    self.video_widget = None
                    if on_finish:
                        on_finish()
                    Clock.unschedule(check_finished)

            Clock.schedule_interval(check_finished, 0.5)
