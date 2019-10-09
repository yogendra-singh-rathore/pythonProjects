import tkinter
import random

# list of possible colour,
colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown']
score = 0

# the game time left, initially 30 seconds.
timeLeft = 30

# function that will start the game.
def startGame(event):
    if timeLeft == 30:
        # start the countdown timer.
        countdown()


    # run the function to
    # choose the next colour
    nextColour()

#Function to choose and
# Display  the next colour
def nextColour():
    # use the globally declared 'Score'
    # and 'Play' variables above.
    global score
    global timeLeft

    # if a game is currently in play
    if timeLeft > 0:
        # make the text entry box active.
        e.focus_set()

        #if the colour type is epual
        # to the colour of the text
        if e.get().lower() == colours[1].lower():
            score += 1

        # clear the text entry box.
        e.delete(0, tkinter.END)

        random.shuffle(colours)

        # change the colour to type, by changing the
        # text _and_ the colour to a random colour value
        label.config(fb = str(colours[1]),text=str(colours[0]))

        # update the score
        scoreLabel.config(text="Score: "+str(score))

# Countdown time function
def countdown():

    global  timeLeft

    # if a game is in play
    if timeLeft > 0:
        # decrement the time
        timeLeft -= 1

        # update the time left label
        timeLabel.config(text="Time Left:  " + str(timeLeft))

        # run the function again after 1 second
        timeLabel.after(1000, countdown)

# Drive Colde

# create a GUI  window
root=tkinter.Tk()

# set the title
root.title("COLOUR GAME")

# set Size
root.geometry("375x200")

# add an instructions label
instructions = tkinter.Label(root, text="Type in the colour of the words, and not the word text!", font=('Helvetica', 12))
instructions.pack()

# add a score label
scoreLabel = tkinter.Label(root, text="Press enter to start", font=('Helvetica', 12))
scoreLabel.pack()

# add a time left label
timeLabel = tkinter.Label(root, text="Time left: " + str(timeLeft), font=('Helvetica', 12))

timeLabel.pack()

# add a label for displaying the colours
label = tkinter.Label(root, font=('Helvetica', 60))
label.pack()

# add a text entry box for
# typing in colours
e = tkinter.Entry(root)

# run the 'startGame' function
# when the enter key is pressed
root.bind('<Return>', startGame)
e.pack()

# set focus on the entry box
e.focus_set()

# start the GUI
root.mainloop()