# coding=utf-8
import tkinter as tk


def main() -> None:
    app = tk.Tk()
    app.title("BlockCoinMiner")
    app.configure(width=700, height=500, bg="#797979")
    app.resizable(width=False, height=False)
    app.iconbitmap("icon.ico")
    app.mainloop()

if __name__ == "__main__":
    main()
