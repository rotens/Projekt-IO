import tkinter as tk

from game_interface import GameInterface

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    GameInterface(root)
    root.mainloop()
