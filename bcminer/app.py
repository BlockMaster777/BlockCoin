# coding=utf-8
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from bcminer.api import Generator, InvalidTokenException, Token, remove_id_from_token_tuple, save_tokens_to_db
from bcminer import db_manager


app = tk.Tk()
app.title("BlockCoinMiner")
app.configure(width=700, height=550)
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
    current_list.delete(0, tk.END)
    threading.Thread(target=mining_process, args=(count, owner), daemon=True).start()

def export_all_tokens_to_file():
    tokens = all_list.get(0, tk.END)
    with (filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("txt", "TXT")], title="Export tokens")
          as f):
        if f:
            f.write(" ".join(tokens))

def import_all_tokens_from_file():
    with (filedialog.askopenfile(defaultextension=".txt", filetypes=[("txt", "TXT")], title="Import tokens")
          as f):
        if f:
            def try_from_string(tok_string):
                try:
                    return Token.from_string(tok_string)
                except InvalidTokenException:
                    return None
            tokens = [try_from_string(tok_string) for tok_string in f.read().split()]
            save_tokens_to_db(tokens)
            all_list.delete(0, tk.END)
            all_list.insert(tk.END, *[str(Token(*remove_id_from_token_tuple(tok_tuple)))
                                      for tok_tuple in dbm.get_tokens()])

def clear_all_tokens():
    if tk.messagebox.askyesno("Confirm", "Are you sure you want to clear all tokens? This action cannot be undone."):
        dbm.clear_tokens()
        all_list.delete(0, tk.END)


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

ttk.Button(app, text="Copy current tokens", command=lambda: app.clipboard_append(" ".join(
        current_list.get(0, tk.END)))).place(x=20, y=500)

ttk.Button(app, text="Export all tokens", command=export_all_tokens_to_file).place(x=220, y=500)

ttk.Button(app, text="Import all tokens", command=import_all_tokens_from_file).place(x=380, y=500)

ttk.Button(app, text="Clear all tokens", command=clear_all_tokens).place(x=540, y=500)

app.mainloop()
