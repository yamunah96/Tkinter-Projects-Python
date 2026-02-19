import tkinter as tk
import random

# Create window
root = tk.Tk()
root.title("Dice Roll Game")
root.geometry("400x400")
root.config(bg="white")

# Scores
user_score = 0
ai_score = 0

# Title
title = tk.Label(root, text="Dice Roll Game", font=("Arial", 20, "bold"), fg="blue", bg="white")
title.pack(pady=20)

# Scoreboard
score_label = tk.Label(root, text="Player: 0  |  AI: 0", font=("Arial", 16), fg="black", bg="white")
score_label.pack(pady=10)

# Dice result labels
result_frame = tk.Frame(root, bg="white")
result_frame.pack(pady=20)

user_roll_label = tk.Label(result_frame, text="Player Roll: -", font=("Arial", 14), bg="white")
user_roll_label.grid(row=0, column=0, padx=30)

ai_roll_label = tk.Label(result_frame, text="AI Roll: -", font=("Arial", 14), bg="white")
ai_roll_label.grid(row=0, column=1, padx=30)

# Result message
winner_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="green", bg="white")
winner_label.pack(pady=20)

# Game Logic
def roll_dice():
    global user_score, ai_score

    user_roll = random.randint(1, 6)
    ai_roll = random.randint(1, 6)

    user_roll_label.config(text=f"Player Score: {user_roll}")
    ai_roll_label.config(text=f"AI Score: {ai_roll}")

    if user_roll > ai_roll:
        winner = "You Win!"
        user_score += 1
    elif ai_roll > user_roll:
        winner = "AI Wins!"
        ai_score += 1
    else:
        winner = "It's a Draw!"

    winner_label.config(text=winner)
    score_label.config(text=f"You: {user_score}  |  AI: {ai_score}")

# Roll Button
roll_button = tk.Button(root, text="Roll Dice", font=("Arial", 14), bg="#7b68ee", fg="white", command=roll_dice)
roll_button.pack(pady=10)

# Run the game loop
root.mainloop()
