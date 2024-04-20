import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, root, update_callback):
        bg_color = "#27212E"
        text_color = "#FFFFFF"
        tk.Frame.__init__(self, root, width=200, highlightbackground="black", highlightthickness=1, bg=bg_color)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # API Key
        self.key_label = tk.Label(self, text="Enter NewsAPI api key:", bg=bg_color, fg=text_color)
        self.key_label.pack()
        self.key_entry = tk.Entry(self)
        self.key_entry.pack()

        # Search Querty
        self.query_label = tk.Label(self, text="Search query:", bg=bg_color, fg=text_color)
        self.query_label.pack()
        self.query_entry = tk.Entry(self)
        self.query_entry.pack()

        # Category options
        self.category_label = tk.Label(self, text="Select Categories:", bg=bg_color, fg=text_color)
        self.category_label.pack()

        categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        check_buttons = []
        check_vars = []
        for i in range(len(categories)):
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self, variable=v, text=categories[i].title(), width=15, anchor=tk.W, 
                                bg=bg_color, fg=text_color, selectcolor='black',
                                command=update_callback).pack()
            check_buttons.append(cb)
            check_vars.append(v)

        self.check_buttons = check_buttons
        self.check_vars = check_vars

        test = [str(cb.get()) for cb in self.check_vars]
        self.test = test
        

class ContentFrame(tk.Frame):
    def __init__(self, root):
        bg_color = "#FFF1C8"
        tk.Frame.__init__(self, root, width=400, highlightbackground="black", highlightthickness=1, bg=bg_color)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.test_label = tk.Label(self, text="Content Window:", bg=bg_color)
        self.test_label.pack()

class MainApp:
    __apikey = ""

    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("News Aggregator")

        self.left_frame = MenuFrame(root, self.update_category_selections)
        self.left_frame.pack_propagate(False)
        self.right_frame = ContentFrame(root)
        self.right_frame.pack_propagate(False)

        # Show selections
        self.category_label = tk.Label(self.right_frame, text="Selected options: " + ", ".join(self.left_frame.test))
        self.category_label.pack()

    def update_category_selections(self):
        options = [str(var.get()) for var in self.left_frame.check_vars if var.get()]
        self.category_label.config(text="Selected options: " + ", ".join(options))

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
