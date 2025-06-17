import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt
import vlc
import speech_recognition as sr
import json

# Load story pages
with open("pages.json", "r") as f:
    story_pages = json.load(f)

class StoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle("Story Reader")
        self.setGeometry(100, 100, 800, 480)
        self.current_page = 0

        # VLC Media Player
        self.player = vlc.MediaPlayer("background_music.mp3")
        events = self.player.event_manager()
        self.player.play()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.loop_music)

        # Volume buttons
        self.mute_button = QPushButton("Mute")
        self.mute_button.setFixedSize(60, 30)
        self.mute_button.clicked.connect(lambda: self.set_volume(0))

        self.vol_down_button = QPushButton("–")
        self.vol_down_button.setFixedSize(30, 30)
        self.vol_down_button.clicked.connect(self.decrease_volume)

        self.vol_up_button = QPushButton("+")
        self.vol_up_button.setFixedSize(30, 30)
        self.vol_up_button.clicked.connect(self.increase_volume)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet(
            "font-weight: bold; font-size: 18px; color: red; background: transparent; border: none;"
        )

        # Top bar layout (right-aligned)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.mute_button)
        top_bar_layout.addWidget(self.vol_down_button)
        top_bar_layout.addWidget(self.vol_up_button)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.close_button)

        # Text area 
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("font-size: 20px;")
        self.text_area.setText(story_pages[self.current_page])

        #rec section
        self.record_button = QPushButton("Record Speech")
        self.record_button.clicked.connect(self.record_speech)

        self.recognized_text = QTextEdit()
        self.recognized_text.setReadOnly(True)
        self.recognized_text.setPlaceholderText("...")

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)

        rec_layout = QHBoxLayout()
        rec_layout.addWidget(self.record_button)
        rec_layout.addWidget(self.recognized_text)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_button)
        btn_layout.addWidget(self.next_button)

        # Main vertical layout: top bar, text area, buttons
        layout = QVBoxLayout()
        layout.addLayout(top_bar_layout)
        layout.addWidget(self.text_area, stretch=3)
        layout.addLayout(rec_layout,stretch=1)
        layout.addLayout(btn_layout)

        container = QWidget()
container.setObjectName("CentralWidget")
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.current_volume = 50
        self.set_volume(self.current_volume)

    def next_page(self):
        if self.current_page < len(story_pages) - 1:
            self.current_page += 1
            self.text_area.setText(story_pages[self.current_page])

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_area.setText(story_pages[self.current_page])

    def loop_music(self, event):
        self.player.stop()
        self.player.play()

    def set_volume(self, level):
        self.player.audio_set_volume(max(0, min(100, level)))
        self.current_volume = level

    def increase_volume(self):
        self.set_volume(self.current_volume + 10)

    def decrease_volume(self):
        self.set_volume(self.current_volume - 10)

    def record_speech(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        self.recognized_text.setText("Listening...")

        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            self.recognized_text.setText(text)
        except sr.UnknownValueError:
            self.recognized_text.setText("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            self.recognized_text.setText(f"API error: {e}")
        except Exception as e:
            self.recognized_text.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoryApp()
    window.showFullScreen()
    sys.exit(app.exec_())
