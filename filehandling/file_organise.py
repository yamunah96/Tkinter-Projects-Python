import os
import shutil
import time 

from tkinter import filedialog, messagebox
import tkinter as tk

file_types = {
    'Images': ['.jpg', '.jpeg', '.png'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Videos': ['.mp4', '.mov'],
    'Others': []
}

def OrganiseFiles(folder):
    if not os.path.exists(folder):
        messagebox.showerror(title="error", message="This folder does not exist")
        return
    

    # create subfolder if they dont exists
    for category in file_types:
        category_path= os.path.join(folder,category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    
    #  folder contain  5 or 6 files
    myfiles= os.listdir(folder)
    for file_name in myfiles:
        file_path= os.path.join(folder,file_name)

        if os.path.isdir(file_path):
            continue

        file_extension= os.path.splitext(file_name)[1].lower()
        # print(file_extension)
        file_moved=False

        for category,extension in file_types.items():
            if file_extension in extension:  #C:\Users\Mamatha-Win10\Downloads\testing
                dest_path= os.path.join(folder,category,file_name)
                print(file_path,dest_path)
                shutil.move(file_path,dest_path)
                file_moved=True
                break
        if not file_moved:
            dest_path= os.path.join(folder,"Others",file_name)
            shutil.move(file_path,dest_path)
    messagebox.showinfo(title="success", message="This folder is organised succesfully")
    

def startorganising():
    folder=folderpath.get()
    OrganiseFiles(folder)

def browsefolder():
    folderselected = filedialog.askdirectory()
    if folderselected:
        folderpath.set(folderselected)

window = tk.Tk()
window.configure(bg="blue")
window.title("File Organiser")
window.geometry("500x500")
heading=tk.Label(window,text="File Organiser",font=("Ariel",25))
heading.pack(pady=7)
text1=tk.Label(window,text="Select Folder to Organize: ",font=("Ariel",12))
text1.pack(pady=7)
folderpath=tk.StringVar()
textbox=tk.Entry(window,textvariable=folderpath, width=50)
textbox.pack(pady=7)
browsebutton=tk.Button(window,text="Browse",command=browsefolder)
browsebutton.pack(pady=7)
organisebutton=tk.Button(window,text="Organise",bg="green",fg="white",command=startorganising)
organisebutton.pack(pady=7)



window.mainloop()

