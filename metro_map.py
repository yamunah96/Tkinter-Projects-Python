import tkinter as tk

class MetroFareCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Metro Map")
        self.root.configure(bg='Darkgreen')
        self.root.geometry("600x600+10+0")

        self.stn_sL = ['SpriteLand', 'GoNGlide', 'Costumes', 'Broadcast', 'Python', 'Cloning', 'MyBlocks']
        self.stn_pL = ['EscapeChar', 'WhileLoop', 'Python', 'IfElifElse', 'Range', 'Dictionary', 'TurtlePark']
        
        self.create_canvas()
        self.draw_lines()
        self.create_dropdowns()
        self.create_buttons_and_labels()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=550, height=500)
        self.canvas.pack()

    def draw_lines(self):
        # Draw Scratch Line (left to right)
        self.draw_line(self.stn_sL, 50, 200, 70, 0, 0, 30, 'DarkOrange')

        # Draw Python Line (top to bottom)
        self.draw_line(self.stn_pL, 330, 40, 0, 70, 35, 0, 'blue')


    def draw_line(self, stations, start_x, start_y, step_x, step_y, label_dx, label_dy, color):
        x = start_x
        y = start_y
        radius = 6

        for i in range(len(stations)):
            if i < len(stations) - 1:
                # Draw line to next station
                self.canvas.create_line(x, y, x + step_x, y + step_y, fill=color)

            # Draw station circle
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

            # Add station name
            self.canvas.create_text(x + label_dx, y + label_dy, text=stations[i], fill=color, font=('Helvetica', 6, 'bold'))

            # Move to next station
            x += step_x
            y += step_y


    def create_dropdowns(self):
        # Prepare station list without 'Python'
        self.all_stations = list(set(self.stn_sL + self.stn_pL))
        self.all_stations.remove('Python')

        self.canvas.create_text(30, 460, text='Start', fill='white')
        self.start_station = tk.StringVar()
        self.drop_start = tk.OptionMenu(self.root, self.start_station, *self.all_stations)
        self.drop_start.place(x=30, y=470)

        self.canvas.create_text(240, 460, text='Stop', fill='white')
        self.stop_station = tk.StringVar()
        self.drop_stop = tk.OptionMenu(self.root, self.stop_station, *self.all_stations)
        self.drop_stop.place(x=240, y=470)

    def create_buttons_and_labels(self):
        self.button = tk.Button(text="Calculate Fare", command=self.calculate_fare)
        self.button.pack()

        self.fare_label = tk.Label(self.root, text='FARE = ', font=('Helvetica 12 bold'))
        self.fare_label.pack()

    def calculate_fare(self):
        start = self.start_station.get()
        stop = self.stop_station.get()

        if not start or not stop:
            self.fare_label.configure(text="Please select both stations.")
            return

        # Determine which line the stations belong to
        if start in self.stn_sL:
            start_line = self.stn_sL
        else:
            start_line = self.stn_pL

        if stop in self.stn_sL:
            stop_line = self.stn_sL
        else:
            stop_line = self.stn_pL
            
        # Calculate number of stops

       # Count number of stops
        if start_line == stop_line:
            # Both stations are on the same line
            n_stops = abs(start_line.index(start) - start_line.index(stop))
        else:
            # Stations are on different lines, change at map
            stops_to_interchange = abs(start_line.index(start) - start_line.index('Python'))
            stops_from_interchange = abs(stop_line.index('Python') - stop_line.index(stop))
            n_stops = stops_to_interchange + stops_from_interchange

        fare = n_stops * 20
        self.fare_label.configure(text=f'FARE = INR {fare}')


# Run the application
if __name__ == "__main__":
    window = tk.Tk()
    app = MetroFareCalculator(window)
    window.mainloop()
