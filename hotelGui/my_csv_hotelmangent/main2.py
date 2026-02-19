import tkinter as tk
import csv
import os


#INITIAL VARIABLES
pitch_black = "#3B3B3B"
gray = "#535353"
white = "#FFFFFF"
cyan = "#00FFFF"
custom_font = ("Courier New", 18)
custom_font_small = ("Courier New", 16)
x = 15
y = 15
w = 10  

room_types = {"Standard Room" : 90, "Standard Room +AC" : 110, "Double Room" : 175, "Deluxe Room" : 255, "Luxury Room" : 400}
#APPLICATION CODE
window = tk.Tk()
window.geometry("1250x750")
window.resizable(width = False, height = False)
window.configure(bg = pitch_black)

entry_frame = tk.Frame(bg = gray)
entry_frame.pack()
button_frame = tk.Frame(bg = gray)
button_frame.pack(pady = y)
room_type = tk.StringVar()
room_type.set("Standard Room")
guests = []
guest_string = ""
def save_data():    
    if not os.path.exists("guests.csv"):        
        with open("guests.csv", "w") as file:           
            writer = csv.DictWriter(file, fieldnames = ["name", "room_number", "total_days", "room_type", "avaliability"])            
            writer.writeheader()   
    else:        
        with open("guests.csv", "w", newline = "") as file:            
            writer = csv.DictWriter(file, fieldnames = ["name", "room_number", "total_days", "room_type", "avaliability"])            
            writer.writeheader()            
            for guest in guests:                
                writer.writerow(guest)
def add_guest():    
    global guest_string
    if name_entry.get() == "":        
        print("Error")        
        return    
    if not room_number_entry.get().isdigit() or not total_days_entry.get().isdigit():        
        print("Error")       
        return        
    guest = {"name" : name_entry.get(),            
            "room_number" : int(room_number_entry.get()),            
            "total_days" : int(total_days_entry.get()),             
            "room_type" : room_type.get(),            
            "avaliability" : False}    
    guests.append(guest)
    guest_display.configure(state = "normal")    
    guest_display.insert(tk.END, f"Name: {guest["name"]}  Room Number: {guest["room_number"]}  Total Days: {guest["total_days"]}  Room Type: {guest["room_type"]}  Avaliability: {guest["avaliability"]}\n")    
    guest_string += str(guest)
    name_entry.delete(first = 0, last = tk.END)    
    room_number_entry.delete(first = 0, last = tk.END)    
    total_days_entry.delete(first = 0, last = tk.END)

def search_guest(name, room_number):    
    with open("guests.csv", "r") as file:        
        reader = csv.DictReader(file)        
        for row in reader:            
            if row["name"] == name or row["room_number"] == room_number:                
               print(row)
        return False
    



tk.Label(master = entry_frame, text = "Name:", fg =  white, bg = gray, font = custom_font).grid(row = 0, column = 0, padx = x, pady = y)
tk.Label(master = entry_frame, text = "Room Number:", fg =  white, bg = gray, font = custom_font).grid(row = 1, column = 0, padx = x, pady = y)
tk.Label(master = entry_frame, text = "Total Days:", fg =  white, bg = gray, font = custom_font).grid(row = 2, column = 0, padx = x, pady = y)
tk.Label(master = entry_frame, text = "Room Type:", fg =  white, bg = gray, font = custom_font).grid(row = 3, column = 0, padx = x, pady = y)


name_entry = tk.Entry(master = entry_frame, fg = white, bg = pitch_black, font = custom_font, borderwidth = 2)
name_entry.grid(row = 0, column = 1, pady = y)
room_number_entry = tk.Entry(master = entry_frame, fg = white, bg = pitch_black, font = custom_font, borderwidth = 2)
room_number_entry.grid(row = 1, column = 1, pady = y)
total_days_entry = tk.Entry(master = entry_frame, fg = white, bg = pitch_black, font = custom_font, borderwidth = 2)
total_days_entry.grid(row = 2, column = 1, pady = y)
room_type_option = tk.OptionMenu(entry_frame, room_type, *room_types.keys())
room_type_option.configure(fg = white, bg = pitch_black, font = custom_font)
room_type_option.grid(row = 3, column = 1)

add_button = tk.Button(master = button_frame, text = "Add Guest", fg = white, bg = pitch_black, font = custom_font, width = w, command = add_guest)
add_button.grid(row = 0, column = 0, pady = y)
save_button = tk.Button(master = button_frame, text = "Save (CSV)", fg = white, bg = pitch_black, font = custom_font, width = w, command = save_data)
save_button.grid(row = 1, column = 0, pady = y)
search_button = tk.Button(master = button_frame, text = "Search Guest", fg = white, bg = pitch_black, font = custom_font, width = w, command =search_guest("yamuna",2))
search_button.grid(row = 0, column = 1, pady = y)
guest_display = tk.Text(master = window, width = 100, height = 50, fg = white, bg = gray, font = custom_font_small, borderwidth = 2.5)
guest_display.pack(pady = y)
guest_display.configure(state = "disabled")
window.mainloop()

#