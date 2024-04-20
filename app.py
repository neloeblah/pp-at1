import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, root, update_callback):
        self.bg_color = "#27212E"
        self.text_color = "#FFFFFF"
        self.update_callback = update_callback
        
        tk.Frame.__init__(self, root, width=200, highlightbackground="black", highlightthickness=1, bg=self.bg_color)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # API Key
        self.key_label = tk.Label(self, text="Enter NewsAPI api key:", bg=self.bg_color, fg=self.text_color)
        self.key_label.pack()
        self.key_entry = tk.Entry(self)
        self.key_entry.pack()

        # Search Query
        self.query_label = tk.Label(self, text="Search query:", bg=self.bg_color, fg=self.text_color)
        self.query_label.pack()
        self.query_entry = tk.Entry(self)
        self.query_entry.pack()

        # Category options
        self.category_label = tk.Label(self, text="Select Categories:", bg=self.bg_color, fg=self.text_color)
        self.category_label.pack()

        self.create_category_menu()
        
    def create_category_menu(self):
        categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        check_buttons = []
        check_vars = []

        for i in range(len(categories)):
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self, variable=v, text=categories[i].title(), width=15, anchor=tk.W, 
                                bg=self.bg_color, fg=self.text_color, selectcolor='black',
                                command=self.update_callback).pack()
            check_buttons.append(cb)
            check_vars.append(v)

        self.check_buttons = check_buttons
        self.check_vars = check_vars
        

class ContentFrame(tk.Frame):
    def __init__(self, root):
        bg_color = "#FFF1C8"
        tk.Frame.__init__(self, root, width=400, highlightbackground="black", highlightthickness=1, bg=bg_color)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.test_label = tk.Label(self, text="Content Window:", bg=bg_color)
        self.test_label.pack()


class MainApp:
    __api_key = ""

    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("News Aggregator")

        # Menu
        self.left_frame = MenuFrame(root, self.update_category_selections)
        self.left_frame.pack_propagate(False)
        self.left_frame.key_entry.bind("<Return>", self.set_api_key)

        # Content
        self.right_frame = ContentFrame(root)
        self.right_frame.pack_propagate(False)

        # Show selections
        self.category_label = tk.Label(self.right_frame, text="")
        self.update_category_selections()
        self.category_label.pack()

    def set_api_key(self, event):
        MainApp.__api_key = self.left_frame.key_entry.get()
        self.left_frame.key_entry.delete(0, tk.END)

    def update_category_selections(self):
        options = [str(var.get()) for var in self.left_frame.check_vars if var.get()]
        self.category_label.config(text="Selected options: " + ", ".join(options))


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
