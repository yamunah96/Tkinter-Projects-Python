import tkinter as tk
from tkinter import messagebox
from user_db import UserDatabase

# Create DB object globally
db = UserDatabase()


# Main Application Class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("400x300")
        self.resizable(False, False)
        self.logged_in_user = None  # Track current user

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (SignInScreen, SignUpScreen, MainScreen):
            # print(F)
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(SignInScreen)

    def show_frame(self, screen_class):
        frame = self.frames[screen_class]
        if screen_class == MainScreen:
            frame.update_username_display(self.logged_in_user)
        frame.tkraise()

# Sign In Screen
class SignInScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Sign In", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Sign In", command=self.sign_in).pack(pady=10)
        tk.Button(self, text="Go to Sign Up", command=lambda: controller.show_frame(SignUpScreen)).pack()

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if db.validate_user(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.controller.logged_in_user = username
            self.controller.show_frame(MainScreen)
        else:
            messagebox.showerror("Error", "Invalid credentials")

# Sign Up Screen
class SignUpScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Sign Up", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Sign Up", command=self.sign_up).pack(pady=10)
        tk.Button(self, text="Go to Sign In", command=lambda: controller.show_frame(SignInScreen)).pack()

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if db.user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
        elif not username or not password:
            messagebox.showwarning("Warning", "Please fill all fields.")
        else:
            db.add_user(username, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.controller.logged_in_user = username
            self.controller.show_frame(MainScreen)

# Main App Screen
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.user_label = tk.Label(self, text="", font=("Arial", 12), anchor="e")
        self.user_label.pack(anchor="ne", padx=10, pady=5)

        tk.Label(self, text="Welcome to Main Screen!", font=("Arial", 18)).pack(pady=40)
        tk.Button(self, text="Logout", command=self.logout).pack()

    def update_username_display(self, username):
        self.user_label.config(text=f"👤 {username}")

    def logout(self):
        self.controller.logged_in_user = None
        self.controller.show_frame(SignInScreen)

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
