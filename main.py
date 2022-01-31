from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
PINK = "#e2979c"

# ----------------------------------------------- MECHANISM --------------------------------------------------#

# csv read
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def known_card():
    to_learn.remove(current_card)
    data_file = pandas.DataFrame(to_learn)
    data_file.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------------------------------- UI SETUP ------------------------------------------------------#

# window setup

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# canvas setup for front
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="French", font=("Courier", 60, "bold"))
card_word = canvas.create_text(400, 263, text="", font=("Courier", 30, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# ---------------------------------------------------- BUTTONS -------------------------------------------------------#

# right_button

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, command=known_card)
right_button.grid(row=1, column=1)
right_button.config(padx=50, pady=20)

# wrong_button

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

# keeps the window on

window.mainloop()

# ---------------------------------------------------- END -------------------------------------------------------#
