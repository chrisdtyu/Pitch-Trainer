# main.py
#
# Author: Christopher Yu
# Email: chrisdtyu@gmail.com
#
# Source code for the pitch trainer.

import pygame 
import random
pygame.init()

from tkinter import *

# creating window
window = Tk()
window.geometry("420x600")
window.title("Perfect Pitch Trainer")
window.config(background="#F5F5DC")
window.resizable(False, False)

# creating icon
icon = PhotoImage(file="note.png")
window.iconphoto(True,icon)

# function to retrieve all child widgets of window
def all_children(window):
   _list = window.winfo_children()
   for item in _list:
       if item.winfo_children():
           _list.extend(item.winfo_children())
   return _list

# function to close the window
def close():
  window.destroy()
  window.quit()

# creating an exit button
exit_button = Button(window,text="Exit",font=("Helvetica", 12),command=close,fg="white",
                    bg="red")
exit_button.pack(side=TOP,anchor=NE)

# creating a button to hear the pitch middle C for reference  
def middle_C():
   pygame.mixer.music.load("pitches/C4.mp3")
   pygame.mixer.music.play()

reference = Button(window, text="Middle C", font=("Helvetica", 14), command=middle_C,
                  fg="#00FF00",bg="black",activeforeground="#00FF00",activebackground="black")
reference.pack()

# list containing all 12 semitones in the middle octave of a piano
notes = ["A4","Ab4","B4","Bb4","C4","D4","Db4","E4","Eb4","F4","G4","Gb4"]
ans = int()

# label indicating that the selected note was correct
correct_label = Label(window,text="       Correct! \n\nThe note is:",font=("Helvetica", 22),
                     fg="#00FF00",bg="#F5F5DC",activeforeground="#00FF00",activebackground="#F5F5DC")

# label indicating that the selected note was correct and to try again
try_again = Label(window,text="Try again!",font=("Helvetica", 24),
                 fg="red",bg="#F5F5DC",activeforeground="red",activebackground="#F5F5DC")

# label to display the correct note each time
correct_note = StringVar()
show_note = Label(window,textvariable=correct_note,font=("Helvetica", 22),
                    fg="#00FF00",bg="#F5F5DC",activeforeground="#00FF00",activebackground="#F5F5DC") 


# function that goes through the process of playing a random note, 
# providing options for the user to select, and handling the user's response
def play():
    correct_label.pack_forget()
    try_again.pack_forget()
    global ans
    global random_note
    random_note = random.choice(notes)
    
    # plays a random note
    if random_note == "A4":
        pygame.mixer.music.load("pitches/A4.mp3")
        pygame.mixer.music.play()
        ans = 9
        correct_note.set("A")
    elif random_note == "Ab4":
        pygame.mixer.music.load("pitches/Ab4.mp3")
        pygame.mixer.music.play()
        ans = 8
        correct_note.set("G#/Ab")
    elif random_note == "B4":
        pygame.mixer.music.load("pitches/B4.mp3")
        pygame.mixer.music.play()
        ans = 11
        correct_note.set("B")
    elif random_note == "Bb4":
        pygame.mixer.music.load("pitches/Bb4.mp3")
        pygame.mixer.music.play()
        ans = 10
        correct_note.set("A#/Bb")
    elif random_note == "C4":
        pygame.mixer.music.load("pitches/C4.mp3")
        pygame.mixer.music.play()
        ans = 0
        correct_note.set("C")
    elif random_note == "D4":
        pygame.mixer.music.load("pitches/D4.mp3")
        pygame.mixer.music.play()
        ans = 2
        correct_note.set("D")
    elif random_note == "Db4":
        pygame.mixer.music.load("pitches/Db4.mp3")
        pygame.mixer.music.play()
        ans = 1
        correct_note.set("C#/Db")
    elif random_note == "E4":
        pygame.mixer.music.load("pitches/E4.mp3")
        pygame.mixer.music.play()
        ans = 4
        correct_note.set("E")
    elif random_note == "Eb4":
        pygame.mixer.music.load("pitches/Eb4.mp3")
        pygame.mixer.music.play()
        ans = 3
        correct_note.set("D#/Eb")
    elif random_note == "F4":
        pygame.mixer.music.load("pitches/F4.mp3")
        pygame.mixer.music.play()
        ans = 5
        correct_note.set("F")
    elif random_note == "G4":
        pygame.mixer.music.load("pitches/G4.mp3")
        pygame.mixer.music.play()
        ans = 7
        correct_note.set("G")
    elif random_note == "Gb4":
        pygame.mixer.music.load("pitches/Gb4.mp3")
        pygame.mixer.music.play()
        ans = 6
        correct_note.set("F#/Gb")
    play_button["state"]=DISABLED


    # button to hear the same note again
    def again():
        pygame.mixer.music.load(f"pitches/{random_note}.mp3")
        pygame.mixer.music.play()

    play_again = Button(window, text="Listen Again",font=("Helvetica", 24),command=again,
                        fg="#00FF00",bg="black",activeforeground="#00FF00",activebackground="black")
    play_again.pack(pady=20)


    # switches the state of the play button
    global switch
    def switch():
        play_button["state"] = NORMAL

    # create set of radiobuttons with the possible options for what note the user just heard 
    global box
    def box():
        for index in range(len(options)):
            answer = Radiobutton(frame, text=options[index], variable=x, font=("Arial", 10),
                                    value=index, indicatoron=0, command=choose, fg="#00FF00",
                                    bg="black", activeforeground="#00FF00", activebackground="black"
                                    )
            answer.pack(anchor=W)

    # button to play another note
    global next_note
    def next_note():
        correct_label.place_forget()
        show_note.place_forget()
        play_again.pack_forget()
        play_button["state"]=NORMAL
        next.place_forget()

    # button to confirm if the user wants to continue
    global next
    next = Button(window, text="Continue", font=("Helvetica", 22), command=next_note,
                    fg="#00FF00", bg="black", activeforeground="#00FF00", activebackground="black")

    options = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

    # function to handle logic of what note the user selects
    def choose():
        if (x.get() == ans):
            try_again.place_forget()
            correct_label.place(x=125, y=325)
            show_note.place(x=305,y=391)
            widget_list = all_children(window)
            for item in widget_list:
                item.pack_forget()
            exit_button.pack(side=TOP, anchor=NE)
            reference.pack()
            play_button.pack(pady=20)
            play_button["state"] = DISABLED
            play_again.pack(pady=20)
            next.place(x=160,y=460)
        else:
            correct_label.place_forget()
            try_again.place(x=160, y=400)
            window.after(1000,try_again.place_forget)
            widget_list = all_children(window)
            for item in widget_list:
                item.pack_forget()
            exit_button.pack(side=TOP, anchor=NE)
            reference.pack()
            play_button.pack(pady=20)
            play_again.pack(pady=20)
            window.after(1000,box)

    x = IntVar()

    frame = Frame(window,bg="#F5F5DC")
    frame.place(x=25, y=270)

    for index in range(len(options)):
        answer = Radiobutton(frame, text=options[index], variable=x,font=("Arial",10),
                                value=index, indicatoron=0, command=choose,fg="#00FF00",
                                bg="black", activeforeground="#00FF00", activebackground="black"
                                )
        answer.pack(anchor=W)



# button to play a note
play_button = Button(window, text="Play New Note", font=("Helvetica", 24), command=play,
                    fg="#00FF00",bg="black",activeforeground="#00FF00",activebackground="black"
                    )
play_button.pack(pady=20)


window.mainloop()
