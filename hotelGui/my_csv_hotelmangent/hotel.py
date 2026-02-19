ROOM_PRICES = {
    "Standard, $1000": 1000,
    "AC, $1500": 1500,
    "Luxury, $2500": 2500
}
import csv,os

class Hotel:
    def __init__(self,filename="guest_details.csv"):
        self.guests = []
        self.filename=filename
        self.create_file_is_not_exist()

    def create_file_is_not_exist(self):
        if not os.path.exists(self.filename):
            with open(self.filename,"w",newline="") as f:
                writer= csv.DictWriter(f,fieldnames=['name','room_no','days','room_type'])
                writer.writeheader()

    def guest_exist_file(self,name,room_no):
        with open(self.filename,"r") as f:
            reader= csv.DictReader(f)
            for row in reader:
                if row["name"] == name and row['room_no'] == room_no:
                    return True
        return False

    def add_guest_to_hotel(self, guest):  # guest is a DICTIONARY
        
        if self.guest_exist_file(guest["name"],guest["room_no"]):
            return False
        with open(self.filename,"a",newline="") as f:
                writer= csv.DictWriter(f,fieldnames=['name','room_no','days','room_type'])
                writer.writerow(guest)
        self.guests.append(guest)
        return True
    
    def find_guest(self, name):
        pass
    
    def save_guest_data(self):
       pass
