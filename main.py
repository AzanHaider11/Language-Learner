from tkinter import *
from pandas import *
import random
from functools import partial
import time

BACKGROUND_COLOR = "#B1DDC6"

df = read_csv("./data/french_words.csv")

try:
    df = read_csv("./data/words_to_learn.csv")
    dict = df.to_dict(orient='records')
except FileNotFoundError:
    with open("./data/words_to_learn.csv", "w") as file:
        df = read_csv("./data/french_words.csv")
        df.to_csv("./data/words_to_learn.csv", index=False)
        dict = df.to_dict(orient='records')


set = {}


def finish():
    canvas.itemconfig(title, text="Finished", fill="black")
    canvas.itemconfig(Word, text=":)", fill="black")


def checkmark():
    with open("./data/words_to_learn.csv", "w") as file:
        dict.remove(set)
        if len(dict) == 0:
            finish()
        df = DataFrame(dict)
        df.to_csv("./data/words_to_learn.csv", index=False)


def translate():
    global set
    canvas.itemconfig(image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    eg_word = set['English']
    canvas.itemconfig(Word, text=eg_word, fill="white")


def new_word():
    global timer, set
    try:
        window.after_cancel(timer)
    except ValueError:
        pass
    canvas.itemconfig(image, image=card_front)
    set = random.choice(dict)
    fr_word = set['French']
    canvas.itemconfig(Word, text=fr_word, fill="black")
    canvas.itemconfig(title, text="French", fill="black")
    timer = window.after(3000, translate)



# Window
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
timer = window.after(1)

# Canvas
canvas = Canvas(height=527, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=1, columnspan=2)

# Images
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")
image = canvas.create_image(400, 263, image=card_front)
wrong = PhotoImage(file="./images/wrong.png")
right = PhotoImage(file="./images/right.png")

# Create text
title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
Word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

# Buttons
Button(image=wrong, highlightthickness=0, command=new_word).grid(row=2, column=1)
Button(image=right, highlightthickness=0, command=lambda: [checkmark(), new_word()]).grid(row=2, column=2)

new_word()


window.mainloop()