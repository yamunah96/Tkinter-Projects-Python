import tkinter as tk
import random

# Setup main window
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("400x500")
root.config(bg="white")

# Global score
human_score = 0
ai_score = 0

# Choices
options = ["Rock", "Paper", "Scissors"]

# ---- UI Labels ----
title = tk.Label(root, text="Rock Paper Scissors", font=("Helvetica", 20, "bold"), fg="#6a5acd", bg="white")
title.pack(pady=10)

subtitle = tk.Label(root, text="With Artificial Intelligence", font=("Helvetica", 12), fg="#9370db", bg="white")
subtitle.pack(pady=5)

score_title = tk.Label(root, text="Score", font=("Helvetica", 16, "bold"), fg="#6a5acd", bg="white")
score_title.pack(pady=10)

score_frame = tk.Frame(root, bg="white")
score_frame.pack()

human_score_label = tk.Label(score_frame, text="0", font=("Helvetica", 20), fg="#6a5acd", bg="white")
human_score_label.grid(row=0, column=0, padx=60)

divider = tk.Label(score_frame, text="|", font=("Helvetica", 20), bg="white")
divider.grid(row=0, column=1)

ai_score_label = tk.Label(score_frame, text="0", font=("Helvetica", 20), fg="#6a5acd", bg="white")
ai_score_label.grid(row=0, column=2, padx=60)

human_label = tk.Label(score_frame, text="Human", font=("Helvetica", 12), bg="white")
human_label.grid(row=1, column=0)

ai_label = tk.Label(score_frame, text="AI", font=("Helvetica", 12), bg="white")
ai_label.grid(row=1, column=2)

# Last choices
choice_frame = tk.Frame(root, bg="white")
choice_frame.pack(pady=10)

human_choice_label = tk.Label(choice_frame, text="None", font=("Helvetica", 12), bg="white")
human_choice_label.grid(row=0, column=0, padx=40)

vs_label = tk.Label(choice_frame, text="VS", font=("Helvetica", 12), bg="white")
vs_label.grid(row=0, column=1)

ai_choice_label = tk.Label(choice_frame, text="None", font=("Helvetica", 12), bg="white")
ai_choice_label.grid(row=0, column=2, padx=40)

# Result label
result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="#6a5acd", bg="white")
result_label.pack(pady=20)

# ---- Game Logic ----
count=0
def play(choice):
    global human_score, ai_score,count
    ai = random.choice(options)

    count+=1

    human_choice_label.config(text=choice)
    ai_choice_label.config(text=ai)

    if choice == ai:
        result = "Draw"
    elif (choice == "Rock" and ai == "Scissors") or \
         (choice == "Paper" and ai == "Rock") or \
         (choice == "Scissors" and ai == "Paper"):
        result = "You Win"
        human_score += 1
    else:
        result = "AI Wins"
        ai_score += 1

    human_score_label.config(text=str(human_score))
    ai_score_label.config(text=str(ai_score))
    result_label.config(text=result)
    count_label.config(text="Count: "+str(count))

    if count>=10:
        if ai_score>human_score:
            gameover.config(text="Gamover AI Own the Game: "+str(ai_score))
        else:
            gameover.config(text="Gamover AI Own the Game: "+str(ai_score),bg='white',fg="#7b68ee")
# ---- Buttons ----
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

def create_button(text):
    return tk.Button(button_frame, text=text, font=("Helvetica", 12), bg="#7b68ee", fg="white", width=10, 
                     command=lambda: play(text))

rock_btn = create_button("Rock")
paper_btn = create_button("Paper")
scissors_btn = create_button("Scissors")

rock_btn.grid(row=0, column=0, padx=10)
paper_btn.grid(row=0, column=1, padx=10)
scissors_btn.grid(row=0, column=2, padx=10)

count_label= tk.Label(button_frame,text="Count :"+str(count),font=("Helvetica", 12), bg="#7b68ee", fg="white")
count_label.grid(row=4, column=1,pady=20)

gameover= tk.Label(button_frame,text=" ",font=("Helvetica", 12), bg="#ffffff", fg="white")
gameover.grid(row=5, column=1,pady=20)

# Run the app
root.mainloop()
