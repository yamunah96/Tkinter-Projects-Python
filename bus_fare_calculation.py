import tkinter as tk
from tkinter import ttk, messagebox

# ------------ OOP Classes ---------------------

class BusRoute:
    def __init__(self, name, color, stops, y):
        self.name = name
        self.color = color
        self.stops = stops
        self.y = y  # y-coordinate on canvas

    def draw(self, canvas):
        x_start = 50
        spacing = 120
        for i, stop in enumerate(self.stops):
            x = x_start + i * spacing
            canvas.create_oval(x-5, self.y-5, x+5, self.y+5, fill=self.color)
            canvas.create_text(x, self.y - 15, text=stop, font=('Arial', 10))
            if i > 0:
                canvas.create_line(x - spacing, self.y, x, self.y, fill=self.color, width=3)


class BusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚌 City Bus Route Map")
        self.root.geometry("700x500")
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(root, width=680, height=200, bg="lightblue")
        self.canvas.pack(pady=10)

        # Define Routes
        self.red_route = BusRoute("Red Route", "red", ["Nagasandra", "Jalhalli", "Yestwantpura", "Majestic"], y=60)
        self.green_route = BusRoute("Green Route", "green", ["Jayanagara", "Banashankri", "Jp Nagar", "Electronic City"], y=150)
      
   
        self.red_route.draw(self.canvas)
        self.green_route.draw(self.canvas)

        # All stops list
        self.all_stops = self.red_route.stops + self.green_route.stops

        # Stop Selection
        frame = tk.Frame(root, bg="white")
        frame.pack(pady=10)

        tk.Label(frame, text="Start Stop:", bg="white").grid(row=0, column=0, padx=5)
        self.start_var = ttk.Combobox(frame, values=self.all_stops, state="readonly")
        self.start_var.grid(row=0, column=1)

        tk.Label(frame, text="End Stop:", bg="white").grid(row=0, column=2, padx=5)
        self.end_var = ttk.Combobox(frame, values=self.all_stops, state="readonly")
        self.end_var.grid(row=0, column=3)

        # Fare Button
        tk.Button(root, text="Calculate Fare", command=self.calculate_fare, bg="darkblue", fg="white").pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="white", fg="green")
        self.result_label.pack()

    def calculate_fare(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if not start or not end:
            messagebox.showwarning("Missing", "Please select both stops.")
            return

        red = self.red_route.stops
        green = self.green_route.stops

        if start in red and end in red:
            i1 = red.index(start)
            i2 = red.index(end)
            stops_between = abs(i2 - i1)
            fare = 10 * stops_between

        elif start in green and end in green:
            i1 = green.index(start)
            i2 = green.index(end)
            stops_between = abs(i2 - i1)
            fare = 10 * stops_between

        elif (start in red and end in green) or (start in green and end in red):
            # Cross route
            if start in red:
                mid_index = red.index(start)
                mid_transfer_index = 0  # Assume transfer happens at first green stop
                stops_red = len(red) - mid_index - 1
                stops_green = green.index(end)
            else:
                mid_index = green.index(start)
                mid_transfer_index = 0
                stops_green = len(green) - mid_index - 1
                stops_red = red.index(end)

            total_stops = stops_red + stops_green
            fare = (10 * total_stops) + 5  # ₹5 switching fee

        else:
            self.result_label.config(text="❌ Invalid route combination", fg="red")
            return

        self.result_label.config(text=f"Fare from {start} to {end} is ₹{fare}", fg="green")



# ------------ Run App ---------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = BusApp(root)
    root.mainloop()
