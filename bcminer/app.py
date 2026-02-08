# coding=utf-8
import tkinter as tk
from tkinter import ttk


app = tk.Tk()
app.title("BlockCoinMiner")
app.configure(width=700, height=500)
app.resizable(width=False, height=False)
app.iconbitmap("icon.ico")

ttk.Style().configure("TButton", font=("Arial", 14))

def validate_input(p):
    if p.isdigit():
        return True
    return False

ttk.Label(app, text="Owner", font=("Arial", 14)).place(x=20, y=20)
owner_var = tk.StringVar(app)
ttk.Entry(app, font=("Arial", 14), width=30, textvariable=owner_var).place(x=20, y=55)

ttk.Label(app, text="Count", font=("Arial", 14)).place(x=20, y=90)
count_var = tk.IntVar(app)
ttk.Entry(app, font=("Arial", 14), width=30, validatecommand=(app.register(validate_input), "%P"),
          validate="key", textvariable=count_var).place(x=20, y=125)

ttk.Button(app, text="Start Mining").place(x=20, y=170)

ttk.Label(app, text="Current Tokens", font=("Arial", 14)).place(x=200, y=180)
current_list = tk.Listbox(app, font=("Arial", 5), width=83, height=30)
current_list.place(x=20, y=220)

ttk.Label(app, text="All tokens", font=("Arial", 14)).place(x=380, y=20)
all_list = tk.Listbox(app, font=("Arial", 5), width=70, height=50)
all_list.place(x=380, y=60)
app.mainloop()
