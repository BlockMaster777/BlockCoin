# coding=utf-8
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from bcminer.api import Generator, Token, remove_id_from_token_tuple
from bcminer import db_manager


app = tk.Tk()
app.title("BlockCoinMiner")
app.configure(width=700, height=500)
app.resizable(width=False, height=False)
app.iconbitmap("icon.ico")

ttk.Style().configure("TButton", font=("Arial", 14))

dbm = db_manager.DatabaseManager()

def validate_input(p):
    if p.isdigit():
        return True
    return False

def update_data(status: str, token: Token = None) -> None:
    if status == "new_token":
        app.after(0, lambda: current_list.insert(tk.END, str(token)))
        app.after(0, lambda: all_list.insert(tk.END, str(token)))
        app.after(0, lambda: current_list.yview_moveto(1))
        app.after(0, lambda: all_list.yview_moveto(1))
    elif status == "mining_started":
        app.after(0, lambda: mine_button.config(state=tk.DISABLED, text="Mining..."))
    elif status == "mining_finished":
        app.after(0, lambda: mine_button.config(state=tk.NORMAL, text="Start Mining"))

def mining_process(amount: int, owner: str):
    gen = Generator(update_data)
    gen.generate_valid_tokens(owner, amount)

def start_mining():
    owner = owner_var.get()
    count = count_var.get()
    if not owner:
        tk.messagebox.showerror("Error", "Owner cannot be empty")
        return
    if count <= 0:
        tk.messagebox.showerror("Error", "Count must be a positive integer")
        return
    threading.Thread(target=mining_process, args=(count, owner), daemon=True).start()

ttk.Label(app, text="Owner", font=("Arial", 14)).place(x=20, y=20)
owner_var = tk.StringVar(app)
ttk.Entry(app, font=("Arial", 14), width=30, textvariable=owner_var).place(x=20, y=55)

ttk.Label(app, text="Count", font=("Arial", 14)).place(x=20, y=90)
count_var = tk.IntVar(app)
ttk.Entry(app, font=("Arial", 14), width=30, validatecommand=(app.register(validate_input), "%P"),
          validate="key", textvariable=count_var).place(x=20, y=125)

mine_button = ttk.Button(app, text="Start Mining", command=start_mining)
mine_button.place(x=20, y=170)

ttk.Label(app, text="Current Tokens", font=("Arial", 14)).place(x=200, y=180)
current_list = tk.Listbox(app, font=("Arial", 7), width=66, height=20)
current_list.place(x=20, y=220)

ttk.Label(app, text="All tokens", font=("Arial", 14)).place(x=380, y=20)
all_list = tk.Listbox(app, font=("Arial", 7), width=60, height=32)
all_list.place(x=380, y=64)
all_list.insert(tk.END, *[str(Token(*remove_id_from_token_tuple(tok_tuple)))
                          for tok_tuple in dbm.get_tokens()])
app.mainloop()
