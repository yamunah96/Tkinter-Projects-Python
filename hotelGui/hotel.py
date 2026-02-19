# -------------------- OOP Classes ----------------------
from openpyxl import Workbook
from openpyxl.styles import Font

ROOM_PRICES = {
    "Standard, $1000": 1000,
    "AC, $1500": 1500,
    "Luxury, $2500": 2500
}

class Guest:
    def __init__(self, name, room_no, days,room_type):
        self.name = name
        self.room_no = room_no
        self.days = days
        self.room_type=room_type
        self.rate = ROOM_PRICES[room_type]

    def total_bill(self):
        return self.days * self.rate


class Hotel:
    def __init__(self):
        self.guests = []

    def add_guest(self, guest):
        self.guests.append(guest)

    def get_all_guests(self):
        return self.guests

    def find_guest(self, name):
        return [g for g in self.guests if g.name.lower() == name.lower()]

    def delete_guest(self, name):
        self.guests = [g for g in self.guests if g.name.lower() != name.lower()]

    def save_to_excel(self, filename="hotel_bookings.xlsx"):
        wb = Workbook()
        ws = wb.active
        ws.title = "Bookings"
        ws.append(["Name", "Room No",  "Room Type","Days", "Total Bill"])
        for g in self.guests:
            ws.append([g.name, g.room_no, g.days, g.room_type ,g.total_bill()])

        for cell in ws["1:1"]:
            cell.font = Font(bold=True)
        wb.save(filename)
