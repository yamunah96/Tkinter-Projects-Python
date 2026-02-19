import tkinter as tk
from tkinter import messagebox


from hotel import Hotel,Guest
# -------------------- Functions ----------------------

# ------------------ Room Prices -------------------
ROOM_PRICES = {
    "Standard, $1000": 1000,
    "AC, $1500": 1500,
    "Luxury, $2500": 2500
}

def add_guest():
    name = name_entry.get()
    room = room_entry.get()
    days = days_entry.get()
    room_type = room_type_var.get()

    if name and room and days.isdigit():
        g = Guest(name, room, int(days),room_type)
        hotel.add_guest(g)
        messagebox.showinfo("Success", f"{name} added successfully!")
        
        name_entry.delete(0, tk.END)
        room_entry.delete(0, tk.END)
        days_entry.delete(0, tk.END)
        guests = hotel.get_all_guests()
        if guests:
            output_box.insert(tk.END, "Guest List:\n")
            for g in guests:
                info = f"{g.name} | Room {g.room_no} | {g.days} days | | {g.room_type}  ₹{g.total_bill()}\n"
                output_box.insert(tk.END, info)
        
    else:
        messagebox.showerror("Input Error", "Please enter valid data.")

def view_bookings():
    output_box.delete(1.0, tk.END)
    guests = hotel.get_all_guests()
    if guests:
        output_box.insert(tk.END, "Guest List:\n")
        for g in guests:
            info = f"{g.name} | Room {g.room_no} | {g.days} days | | {g.room_type}  ₹{g.total_bill()}\n"
            output_box.insert(tk.END, info)
    else:
        output_box.insert(tk.END, "No bookings yet.\n")

def search_guest():
    name = name_entry.get()
    result = hotel.find_guest(name)
    output_box.delete(1.0, tk.END)
    if result:
        output_box.insert(tk.END, f"Search Results for '{name}':\n")
        for g in result:
            output_box.insert(tk.END, f"{g.name} | Room {g.room_no} | {g.days} days | {g.room_type} | ₹{g.total_bill()}\n")
    else:
        output_box.insert(tk.END, f"No guest found with name '{name}'\n")

def delete_guest():
    name = name_entry.get()
    result = hotel.find_guest(name)
    if result:
        hotel.delete_guest(name)
        messagebox.showinfo("Deleted", f"Guest '{name}' removed successfully!")
        view_bookings()
    else:
        messagebox.showerror("Error", f"No guest found with name '{name}'")

def save_excel():
    hotel.save_to_excel()
    messagebox.showinfo("Saved", "Data saved to 'hotel_bookings.xlsx'")

# -------------------- GUI Setup ----------------------
hotel = Hotel()

# window
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("550x550")
root.configure(bg="#f0f8ff")

# Labels and Entries
tk.Label(root, text="Guest Name", bg="#f0f8ff").grid(row=0, column=0, pady=5, padx=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Room No", bg="#f0f8ff").grid(row=1, column=0, pady=5, padx=10)
room_entry = tk.Entry(root)
room_entry.grid(row=1, column=1)

tk.Label(root, text="Days", bg="#f0f8ff").grid(row=2, column=0, pady=5, padx=10)
days_entry = tk.Entry(root)
days_entry.grid(row=2, column=1)

tk.Label(root, text="Room Type", bg="#f0f8ff").grid(row=3, column=0, pady=5, padx=10)
room_type_var= tk.StringVar()
room_type_var.set("Standard") # default
room_menu= tk.OptionMenu(root,room_type_var,*ROOM_PRICES.keys())
room_menu.grid(row=3, column=1)

output_box = tk.Text(root, width=60, height=15)
output_box.grid(row=6, column=0, columnspan=3, padx=10, pady=10)


# -------------------- Buttons ----------------------

tk.Button(root, text="Add Guest", command=add_guest).grid(row=4, column=0, pady=10)
tk.Button(root, text="View Bookings", command=view_bookings).grid(row=4, column=1)
tk.Button(root, text="Save to Excel", command=save_excel).grid(row=4, column=2)

tk.Button(root, text="Search Guest", command=search_guest).grid(row=5, column=0, pady=5)
tk.Button(root, text="Delete Guest", command=delete_guest).grid(row=5, column=1)

tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").grid(row=6, column=2, pady=5)

root.mainloop()
