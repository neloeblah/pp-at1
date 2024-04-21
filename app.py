import tkinter as tk

from tkinter import ttk

COUNTRY_OPTIONS = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                   'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
                   'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
                    'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']
LANGUAGE_OPTIONS = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh']
CATEGORY_OPTIONS = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

class DropMenu:
    def __init__(self, root, text, options, pady=(20,5), width=5):
        self.root = root
        self.text = text
        self.options = options
        self.width = width
        self.pady = pady

        # Add default option to dropdown choices
        self.options.insert(0, "")

    def create_label(self):
        self.label = tk.Label(self.root, text=self.text, bg=self.root.bg_color, fg=self.root.text_color)
        self.label.pack(pady=self.pady)

    def create_menu(self):
        option_var = tk.StringVar()
        option_var.set(self.options[0])

        self.menu = ttk.Combobox(self.root, width=self.width, textvariable=option_var, values=self.options)
        self.menu.pack()

class MenuFrame(tk.Frame):
    def __init__(self, root, update_callback):
        self.bg_color = "#27212E"
        self.text_color = "#FFFFFF"
        self.update_callback = update_callback
        
        tk.Frame.__init__(self, root, width=200, highlightbackground="black", highlightthickness=1, bg=self.bg_color)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # API Key
        self.key_label = tk.Label(self, text="NewsAPI api key:", bg=self.bg_color, fg=self.text_color)
        self.key_label.pack(pady=(10, 5))
        self.key_entry = tk.Entry(self)
        self.key_entry.pack()

        # Search Query
        self.query_label = tk.Label(self, text="Search query:", bg=self.bg_color, fg=self.text_color)
        self.query_label.pack(pady=(10, 5))
        self.query_entry = tk.Entry(self)
        self.query_entry.pack()

        # Category options
        self.category_label = tk.Label(self, text="Select Categories:", bg=self.bg_color, fg=self.text_color)
        self.category_label.pack(pady=(20, 5))

        self.create_category_menu()

        # Dropdown menus for country and language
        self.country_menu = DropMenu(self, text="Select Country:", options=COUNTRY_OPTIONS)
        self.language_menu = DropMenu(self, text="Select Language:", options=LANGUAGE_OPTIONS)
        
        for menu in [self.country_menu, self.language_menu]:
            menu.create_label()
            menu.create_menu()

    def create_category_menu(self):
        categories = CATEGORY_OPTIONS
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

    def create_country_menu(self):
        self.country_label = tk.Label(self, text="Select Country:", bg=self.bg_color, fg=self.text_color)
        self.country_label.pack(pady=(20, 5))

        options = [""] + COUNTRY_OPTIONS
        country_var = tk.StringVar()
        country_var.set(options[0])

        self.country_menu = ttk.Combobox(self, width=5, textvariable=country_var, values=options)
        self.country_menu.pack()

    def create_language_menu(self):
        self.language_label = tk.Label(self, text="Select Language:", bg=self.bg_color, fg=self.text_color)
        self.language_label.pack(pady=(20, 5))

        options = [""] + LANGUAGE_OPTIONS

        language_var = tk.StringVar()
        language_var.set(options[0])

        self.language_menu = ttk.Combobox(self, width=5, textvariable=language_var, values=options)
        self.language_menu.pack()


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
