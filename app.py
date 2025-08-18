import os, sys
import shutil
import math
import json
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Extensions = {
    "Images": ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp'],
    "Videos": ['mp4', 'mkv', 'avi', 'mov', 'flv'],
    "Docs": ['pdf', 'docx', 'doc', 'txt', 'pptx', 'xlsx'],
    "Audio": ['mp3', 'wav', 'aac', 'flac', 'ogg'],
    "Zipped": ['zip', 'rar', 'tar', 'gz', '7z'],
    "Code": ['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'php', 'rb', 'go', 'swift', 'ts'],
    "Executables": ['exe', 'msi', 'bat', 'sh', 'app'],
    "Miscellaneous": []
}

def get_category(extension):
    for category, extensions in Extensions.items():
        if extension.lower() in extensions:
            return category
    return "Miscellaneous"  # Default category if no match found

def organize(user_path):
    try:
        list_of_files = os.listdir(user_path)   #saves the list of files in the given path into that variable.
        moved_files = {}

        for file in list_of_files:
            file_path = os.path.join(user_path, file) 
            if not os.path.isfile(file_path):
                continue


            name, extension = os.path.splitext(file) #splits the file name and extension into two parts in a list.
            extension = extension[1:]     #removes the dot from the extension.

            if not extension:
                continue

            category = get_category(extension)
            category_path = os.path.join(user_path, category)

            if not os.path.exists(category_path):
                os.makedirs(category_path)

            try:
                shutil.move(os.path.join(user_path, file), os.path.join(category_path, file))
                moved_files[file] = category
            except PermissionError:
                messagebox.showinfo("Error", f"Could not move {file}. File is in use.")


        # add moved files' info to json
        json_path = os.path.join(user_path, "moved_files.json")
        with open(json_path, 'w') as json_file:
            json.dump(moved_files, json_file, indent=4)

        os.system(f'notepad "{json_path}"')  

        GBs = (1024 * 1024 * 1024)  #convertion of bytes to gigabytes.

        free_Bytes = shutil.disk_usage(user_path)[2] #gets the free space in bytes in the given path.

        free_GBs = free_Bytes / GBs 

        free_gb = math.floor(free_GBs * 100) / 100 #rounds the free space to two decimal points.

        messagebox.showinfo("Success", f"Folders Organized Successfully!\nFree Space: {free_gb} GBs")


    except FileNotFoundError: #error handling just in case the user enters a wrong path.
        messagebox.showinfo("Error", "Please Enter A Valid Path")

def preview_moves(user_path):
    try:
        list_of_files = os.listdir(user_path)
        preview_files = {}

        for file in list_of_files:
            file_path = os.path.join(user_path, file)
            if not os.path.isfile(file_path):
                continue

            name, extension = os.path.splitext(file)
            extension = extension[1:]
            if not extension:
                continue

            category = get_category(extension)
            preview_files[file] = category

        json_path = os.path.join(user_path, "preview_moves.json")
        with open(json_path, 'w') as json_file:
            json.dump(preview_files, json_file, indent=4)

        os.system(f'notepad "{json_path}"')

    except FileNotFoundError:
        messagebox.showinfo("Error", "Please Enter A Valid Path")

window = Tk()
window.geometry("400x450")
window.title("Desktop Tidy")
window.resizable(False, False)
photo = PhotoImage(file=resource_path("folder-invoices.png"))
icon = PhotoImage(file=resource_path("folder-invoices.png"))
window.iconphoto(True, icon)
window.config(background="lightblue")
label = Label(window, 
              text="Desktop Tidy", 
              font=('Arial',30,'bold'),
              fg=('black'), 
              bg=('lightblue'),)

label.pack(pady=30)

entry = Entry(window, width=40, justify='center', font=('Arial', 10), relief='raised', bd='3', )
entry.insert(0, "Enter The Folder Path")
entry.pack(pady=10)

def clear_placeholder(event):
    if entry.get() == "Enter The Folder Path":
        entry.delete(0, END)

entry.bind("<FocusIn>", clear_placeholder)



def openfile():
    filepath = filedialog.askdirectory()
    if filepath:
        entry.delete(0, END)
        entry.insert(0, filepath)

button1 = Button(window, text="Browse")
button1.config(command=openfile, 
              relief='raised', 
              bd='5', 
              bg="#8ab0e2", 
              font=('Arial', 10, 'bold'), 
              fg='black', 
              activebackground="#6a9cd7", 
              activeforeground='black')

button1.pack(pady=10)

def on_organize():
    user_path = entry.get()
    organize(user_path)


button2 = Button(window, text="Organize Folders")
button2.config(command=on_organize, 
              relief='raised', 
              bd='5', 
              bg="#8ab0e2", 
              font=('Arial', 10, 'bold'), 
              fg='black', 
              activebackground="#6a9cd7", 
              activeforeground='black')


button2.pack()

button3 = Button(window, text="Preview File Moves", command=lambda: preview_moves(entry.get()))
button3.config(relief='raised', 
              bd='5', 
              bg="#8ab0e2", 
              font=('Arial', 10, 'bold'), 
              fg='black', 
              activebackground="#6a9cd7", 
              activeforeground='black')
button3.pack(pady=10)


window.mainloop() 