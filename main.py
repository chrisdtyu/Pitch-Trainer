# main.py
#
# Author: Christopher Yu
# Email: chrisdtyu@gmail.com
#
# Source code for the pitch trainer.

import random
import tkinter as tk
from pathlib import Path

import pygame

BASE_DIR = Path(__file__).parent
PITCH_DIR = BASE_DIR / "pitches"

BEIGE = "#F5F5DC"
BLACK = "black"
GREEN = "#00FF00"
DARK_GREEN = "#007A00"
RED = "#CC0000"
TEXT = "#222222"
HOVER_BG = "#333333"
DISABLED_BG = "#B5B5A5"
DISABLED_FG = "#777769"

# list containing all 12 semitones in the middle octave of a piano
OPTIONS = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

# indexes the pitches 
NOTES = {
    "C4": 0, "Db4": 1, "D4": 2, "Eb4": 3, "E4": 4, "F4": 5,
    "Gb4": 6, "G4": 7, "Ab4": 8, "A4": 9, "Bb4": 10, "B4": 11,
}

OPTION_COLUMNS = 4


def play_pitch(name):
    pygame.mixer.music.load(str(PITCH_DIR / f"{name}.mp3"))
    pygame.mixer.music.play()


class FlatButton(tk.Label):
    """A label that behaves like a button.

    tk.Button ignores background colors on macOS, so this keeps the colors (and the
    red/green answer highlights) consistent across platforms.
    """

    def __init__(self, parent, text, command, font, bg=BLACK, fg=GREEN, hover_bg=HOVER_BG,
                 padx=12, pady=6):
        super().__init__(parent, text=text, font=font, padx=padx, pady=pady)
        self.command = command
        self.base_bg = bg
        self.base_fg = fg
        self.hover_bg = hover_bg
        self.enabled = True
        self.tone = None  
        self.hovering = False

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda _: self._set_hover(True))
        self.bind("<Leave>", lambda _: self._set_hover(False))
        self._refresh()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self._refresh()

    def set_tone(self, tone):
        self.tone = tone
        self._refresh()

    def _set_hover(self, hovering):
        self.hovering = hovering
        self._refresh()

    def _on_click(self, _event):
        if self.enabled:
            self.command()

    def _refresh(self):
        if self.tone == "correct":
            bg, fg = DARK_GREEN, "white"
        elif self.tone == "wrong":
            bg, fg = RED, "white"
        elif not self.enabled:
            bg, fg = DISABLED_BG, DISABLED_FG
        else:
            bg, fg = (self.hover_bg if self.hovering else self.base_bg), self.base_fg
        self.config(bg=bg, fg=fg, cursor="hand2" if self.enabled else "arrow")


class PitchTrainer:
    def __init__(self, window):
        self.window = window
        self.current_note = None
        self.awaiting_answer = False
        self.first_try = True
        self.correct_count = 0
        self.total_count = 0
        self.streak = 0

        window.geometry("420x600")
        window.title("Perfect Pitch Trainer")
        window.config(background=BEIGE)
        window.resizable(False, False)
        window.iconphoto(True, tk.PhotoImage(file=str(BASE_DIR / "note.png")))

        self._build_widgets()

    def _build_widgets(self):
        window = self.window

        top_bar = tk.Frame(window, bg=BEIGE)
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.score_label = tk.Label(top_bar, font=("Helvetica", 14), fg=TEXT, bg=BEIGE)
        self.score_label.pack(side=tk.LEFT)
        FlatButton(top_bar, "Exit", window.destroy, ("Helvetica", 12), bg=RED, fg="white",
                   hover_bg="#B30000", padx=10, pady=2).pack(side=tk.RIGHT)

        FlatButton(window, "Middle C", lambda: play_pitch("C4"),
                   ("Helvetica", 14)).pack(pady=(20, 0))

        self.play_button = FlatButton(window, "Play New Note", self.play_new_note,
                                      ("Helvetica", 24), padx=20, pady=8)
        self.play_button.pack(pady=(20, 0))

        self.listen_again_button = FlatButton(window, "Listen Again", self.listen_again,
                                              ("Helvetica", 18))
        self.listen_again_button.pack(pady=(14, 0))
        self.listen_again_button.set_enabled(False)

        # feedback line
        self.status_label = tk.Label(window, font=("Helvetica", 20), fg=TEXT, bg=BEIGE,
                                     height=2)
        self.status_label.pack(pady=(14, 0))

        # the 12 answer choices in a grid
        options_frame = tk.Frame(window, bg=BEIGE)
        options_frame.pack(pady=(4, 0))
        self.option_buttons = []
        for index, label in enumerate(OPTIONS):
            button = FlatButton(options_frame, label, lambda i=index: self.answer(i),
                                ("Helvetica", 14), padx=0, pady=8)
            button.config(width=6)
            button.set_enabled(False)
            button.grid(row=index // OPTION_COLUMNS, column=index % OPTION_COLUMNS,
                        padx=4, pady=4)
            self.option_buttons.append(button)

        self._update_score()
        self._set_status("Press Play New Note", TEXT)

    def _set_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    def _update_score(self):
        self.score_label["text"] = (f"Score: {self.correct_count}/{self.total_count}"
                                    f"   Streak: {self.streak}")

    def play_new_note(self):
        if self.awaiting_answer:
            return
        # avoid playing the same note twice in a row
        self.current_note = random.choice([n for n in NOTES if n != self.current_note])
        play_pitch(self.current_note)

        self.awaiting_answer = True
        self.first_try = True
        for button in self.option_buttons:
            button.set_tone(None)
            button.set_enabled(True)
        self.play_button.set_enabled(False)
        self.listen_again_button.set_enabled(True)
        self._set_status("Which note was it?", TEXT)

    def listen_again(self):
        if self.current_note:
            play_pitch(self.current_note)

    def answer(self, index):
        button = self.option_buttons[index]
        if not self.awaiting_answer or not button.enabled:
            return

        if index == NOTES[self.current_note]:
            if self.first_try:
                self.correct_count += 1
                self.total_count += 1
                self.streak += 1
            button.set_tone("correct")
            for other in self.option_buttons:
                other.set_enabled(False)
            self.awaiting_answer = False
            self.play_button["text"] = "Next Note"
            self.play_button.set_enabled(True)
            self._set_status(f"Correct! The note is {OPTIONS[index]}", DARK_GREEN)
        else:
            if self.first_try:
                self.total_count += 1
                self.streak = 0
                self.first_try = False
            button.set_tone("wrong")
            button.set_enabled(False)
            self._set_status("Try again!", RED)
        self._update_score()


def main():
    pygame.mixer.init()
    window = tk.Tk()
    PitchTrainer(window)
    window.mainloop()


if __name__ == "__main__":
    main()
