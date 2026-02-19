import tkinter as tk
from tkinter import messagebox


from hotel import Hotel
# -------------------- Functions ----------------------

# ------------------ Room Prices -------------------
ROOM_PRICES = {
    "Standard, $1000": 1000,
    "AC, $1500": 1500,
    "Luxury, $2500": 2500
}

myhotel= Hotel()

def add_guest():
    name = name_entry.get()
    room_no = room_no_entry.get()
    days = days_entry.get()
    room_type = room_type_var.get()

    if name and room_no.isdigit() and days.isdigit():
        guest_details={
            "name":name,
            "room_no":room_no,
            "days":days,
            "room_type":room_type
        }
        myhotel.add_guest_to_hotel(guest_details)
        messagebox.showinfo("Added successfully",name)
    else:
        messagebox.showerror("Wrong Entry","Enter the correct details")



    

def search_guest():
    pass
def save_csv():
    pass

root = tk.Tk()
root.title("Hotel Management System")
root.geometry("550x550")
root.configure(bg="#f0f8ff")

# Labels and Entries
tk.Label(root, text="Guest Name", bg="#f0f8ff").grid(row=0, column=0, pady=5, padx=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Room No", bg="#f0f8ff").grid(row=1, column=0, pady=5, padx=10)
room_no_entry = tk.Entry(root)
room_no_entry.grid(row=1, column=1)

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

tk.Button(root, text="Add Guest",command=add_guest).grid(row=4, column=0, pady=10)
tk.Button(root, text="View Bookings",).grid(row=4, column=1)
tk.Button(root, text="Save to CSV",).grid(row=4, column=2)

tk.Button(root, text="Search Guest",command= search_guest).grid(row=5, column=0, pady=5)
tk.Button(root, text="Delete Guest",).grid(row=5, column=1)

tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").grid(row=6, column=2, pady=5)

root.mainloop()
