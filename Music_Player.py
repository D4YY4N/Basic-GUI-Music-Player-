import sys
import os
import pygame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QIcon

# Initialize Pygame mixer
pygame.mixer.init()

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(300, 300, 400, 200)
        self.setStyleSheet("background-color: #2C3E50; color: white; font: 14pt 'Arial';")

        # Layout
        self.layout = QVBoxLayout()

        # Play, Pause, Stop buttons
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("background-color: #3498DB; color: white; border-radius: 5px;")
        self.play_button.clicked.connect(self.play_music)
        self.layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setStyleSheet("background-color: #F39C12; color: white; border-radius: 5px;")
        self.pause_button.clicked.connect(self.pause_music)
        self.layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 5px;")
        self.stop_button.clicked.connect(self.stop_music)
        self.layout.addWidget(self.stop_button)

        # File Selection Button
        self.select_file_button = QPushButton("Select Music File")
        self.select_file_button.setStyleSheet("background-color: #1ABC9C; color: white; border-radius: 5px;")
        self.select_file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_button)

        # Current File Label
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.file_label)

        # Set main layout
        self.setLayout(self.layout)

        self.current_music_file = None
        self.is_playing = False
        self.is_paused = False
        self.current_pos = 0  # Store position when paused

        # Timer to update the progress
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

    def select_file(self):
        # Open file dialog to select music file
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Music File", "", "Audio Files (*.mp3 *.wav);;All Files (*)",
                                              options=options)
        if file:
            self.current_music_file = file
            self.file_label.setText(f"Selected: {os.path.basename(file)}")

    def play_music(self):
        if self.current_music_file:
            if self.is_paused:  # Resume from the current position if paused
                pygame.mixer.music.play(start=self.current_pos)
                self.is_paused = False
            else:
                pygame.mixer.music.load(self.current_music_file)
                pygame.mixer.music.play()
            self.is_playing = True
            self.timer.start(1000)  # Update progress every second

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.current_pos = pygame.mixer.music.get_pos() / 1000  # Get the current position in seconds
            self.is_playing = False
            self.timer.stop()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_pos = 0
        self.timer.stop()

    def update_progress(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec_())

