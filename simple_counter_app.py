# packages and module
import tkinter as tk

counter=0
# functions to button

def update_label():
    counter_label.configure(text=str(counter))

def increment():
    global counter
    counter+=1
    update_label()

def decrement():
    global counter
    counter-=1
    update_label()

def reset():
    global counter
    counter=0
    update_label()


# widgets
window= tk.Tk()
window.title("Counter APP")
window.geometry("400x400")
window.configure(bg="black")

# title of the app- Counter App # label widegets
title= tk.Label(window,text="Counter APP",font=("Arial",25),fg="red",bg="black")
title.place(x= 120,y=20)


counter_label= tk.Label(window,text="0", font=("Arial", 40), bg="black",fg="white")
counter_label.place(x=200,y=100)


# buttons (increment and decrement)
increment_button= tk.Button(window,text="Increment",command=increment)
increment_button.place(x=50,y=300)

decrement_button= tk.Button(window,text="Decrement",command=decrement)
decrement_button.place(x=250,y=300)

reset_button= tk.Button(window,text="Reset",command=reset)
reset_button.place(x=150,y=350)


window.mainloop()
