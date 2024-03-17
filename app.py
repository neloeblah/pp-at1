import tkinter as tk

class StatusBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set(self, text):
        self.label.config(text=text)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry("400x300")

        self.statusbar = StatusBar(parent)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)


def main():
    root = tk.Tk()
    app = MainApp(root)
    app.pack(side="top", fill="both", expand=True)
    app.statusbar.set(text="Program has loaded.")
    root.mainloop()


if __name__ == "__main__":
    main()
