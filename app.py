import tkinter as tk

class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
