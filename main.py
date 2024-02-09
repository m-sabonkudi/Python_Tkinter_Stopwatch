from tkinter import *   #imports all classes from tkinter
import winsound         #imports the winsound module which's functions will be used to beep when buttons are pressed

window = Tk()              #this is where we create the screen/window from the TK class in the tkinter module
window.title("STOPWATCH")
window.config(padx=50, pady=50, bg="#B1DDC6")    #sets the x and y paddings which will give space between the canvas and the window

timer = None        #the timer is defined as a global variable because it will be used in more than one function
number = None        #the number is defined as a global variable because it will be used in more than one function
count_min = 0       #defined as a global variable because it will be used in more than one function
count_hour = 0      #defined as a global variable because it will be used in more than one function
is_resume = False   #defined as a global variable because it will be used in more than one function


def reset_():
    """Tries stopping the timer from running, if successful, then sets back the values to 00:00:00, and the text on
    button to 'START', then the start button's command will change back to what it was initially (the 'caller' function)
    because it's command is always changed to the 'resume_' function whenever we click on 'START'. If it fails, i.e. if
    user mistakenly presses on the reset button at the very start, which will produce a value error because at the stage
    , the timer variable is set to 'None', then this exception will be caught, and the function will just pass. Either
    way, the function will finally trigger the Beep method from the 'winsound' class."""
    try:
        window.after_cancel(timer)
    except ValueError:
        pass
    else:
        canvas.itemconfig(counter, text="00:00:00")
        start.config(text="START", command=caller)
    finally:
        winsound.Beep(900, 100)


def pause_():
    """Tries to stop the timer from calling the 'start_' function, if it couldn't, i.e. if for whatever reason, the user
     presses the 'pause' button at the very start, then it will simply pass, because trying to stop the variable 'timer'
     at this stage will comprehensibly produce a value error, since it has no value, i.e. it's set to'None'. Moreover,
     trying to stop the timer from running when it hasn't even run a single time is simply irrational. Ultimately, the
     function will unconditionally trigger the beep method, to indicate that the 'pause' button has been pressed."""
    try:
        window.after_cancel(timer)
    except ValueError:
        pass
    finally:
        winsound.Beep(1500, 100)


def resume_():
    """This function will beep, then stop the 'timer' from running. It will then set the value of our global variable
    is_resume to True (will be discussed in 'start_' function). Then the 'start_' function is called, passing in our
    global variable 'number' as the argument. The number variable is the most important in this function, because
    whenever the 'start_' function is triggered, as the parameter 'second' increases, since it is a parameter, the
    'number' variable holds the most recent value of the 'second'. This way, when the 'resume_' function calls the
    'start_' function, the 'number' function will be passed as the argument in place of the parameter 'second', this
    will always make it continue at the very position it stopped when it last ran. Suppose we didn't use the 'number'
    variable, and we used 1 instead just like when the 'caller' is calling the 'start_', then the 'second' will start
    over from 1 since we asked it to do so (and it has no idea where it stopped), and then will affect the 'count_sec',
    and it will start over again, since we set the value of it to be equal to the parameter 'second', but the minute and
    hour will remain unchanged because nothing seems to be changing their values. So when you come to think of it, the
    variable 'number' is just like a reminder to the 'second' parameter, that when it wants to continue running after it
    stopped, the 'number' variable/argument will tell it 'hey, this is where you stopped', and then it will hand it over
    its last value."""
    global number, timer, is_resume
    winsound.Beep(500, 100)
    window.after_cancel(timer)
    is_resume = True
    start_(number)


def caller():
    """As its name indicates, this is the function that calls the main function, i.e. the 'start_' function. Whenever
    this function is called, it sets the values of the 'count_min' and 'count_hour' each to 0. One may wonder, why
    redefine the values to 0 when we've done it right at the beginning of our snippet? Well, of course, when the program
    runs at first, their values each will be 0 even if we didn't redefine them here, but just like we said, the 'start_'
    function doesn't change the values of either 'count_min' or 'count_hour', but only the second, so what will happen
    if our Stopwatch has been reset, and then the user wants to start it again? Of course neither the value of the
    hour nor the minute will change/start over, so here, we are resetting their values such that when the user starts
    the watch over after reset, the values of the hour and minute will actually go back to start from 0. Also, it would
    be cool to tell our user that the start button has now become the button by which they can resume after they've
    paused their watch, that's exactly what we're doing in the penultimate line, as well as changing the command to the
    'resume_' function since it is now actually resuming our watch, and it was initially this very 'caller' function."""

    global count_min, count_hour
    winsound.Beep(500, 100)
    count_hour = 0
    count_min = 0
    start.config(text="RESUME", command=resume_)
    start_(1)


def start_(second):
    """Master Function!"""
    global count_min, count_hour, number, is_resume
    number = second

    count_sec = second

    if not is_resume:
        if count_sec % 60 == 0:
            count_min += 1

    if not is_resume:
        if count_min % 60 == 0 and count_sec % 60 == 0:
            count_hour += 1

    count_sec %= 60

    count_min %= 60
    count_hour %= 60

    holder_min = count_min
    holder_hr = count_hour

    if count_min < 10:
        count_min = f"0{count_min}"
    if count_hour < 10:
        count_hour = f"0{count_hour}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(counter, text=f"{count_hour}:{count_min}:{count_sec}")
    is_resume = False
    count_min = holder_min
    count_hour = holder_hr
    global timer
    timer = window.after(1000, start_, second + 1)


canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
back_img = PhotoImage(file="card_front.png")
bg = canvas.create_image(400, 263, image=back_img)
title = canvas.create_text(400, 100, text="STOPWATCH", font=("Helvetica", 40, "bold"), fill="green")
counter = canvas.create_text(400, 263, text="00:00:00", font=("Arial", 55))
canvas.grid(column=0, row=0, columnspan=3)

start = Button(text="START", font=("Arial", 20, "bold"), command=caller)
start.grid(column=0, row=1)

pause = Button(text="PAUSE", font=("Arial", 20, "bold"), command=pause_)
pause.grid(column=1, row=1)

reset = Button(text="RESET", font=("Arial", 20, "bold"), command=reset_)
reset.grid(column=2, row=1)

window.mainloop()
