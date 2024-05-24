import tkinter as tk
import datetime
import io
import re
import requests
import webbrowser

from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from newsapi import News, TopHeadlines
from scraper import Scraper
from graph import GraphFrame

COUNTRY_OPTIONS = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                   'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
                   'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
                    'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']
LANGUAGE_OPTIONS = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh']
CATEGORY_OPTIONS = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']


class StatusBar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # Create Label
        self.label = tk.Label(self, anchor=tk.E)
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set(self, text):
        # Change contents of status bar
        self.label.config(text=text)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class DropMenu:
    def __init__(self, root, text, options, pady=(10, 5), width=5):
        self.root = root
        self.text = text
        self.options = options
        self.width = width
        self.pady = pady

        # Add blank default option as menus are optional
        self.options.insert(0, "")

    def create_label(self):
        self.label = tk.Label(self.root, text=self.text, bg=self.root.bg_color, fg=self.root.text_color)
        self.label.pack(pady=self.pady)

    def create_menu(self):
        # Menu Selection
        self.option_var = tk.StringVar()
        self.option_var.set(self.options[0])

        # Create menu
        self.menu = ttk.Combobox(self.root, width=self.width, textvariable=self.option_var, values=self.options)
        self.menu.pack()


class MenuFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color, width, category_callback, search_callback):
        tk.Frame.__init__(self, root, width=width, bg=bg_color)
        self.bg_color = bg_color
        self.text_color = text_color
        self.category_callback = category_callback
        self.search_callback = search_callback
        self.news_type = 1
        self.selected_categories = None
        self.filter_country = None
        self.filter_language = None 
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Stylings for widgets
        style = ttk.Style()
        style.configure('W.TButton', background="#27212E", font=('Calibri', 12, 'bold'))
        header_font = ("TkDefaultFont", 10, "underline")

        # User input for search query
        self.query_label = tk.Label(self, text="Search query:", bg=self.bg_color, fg=self.text_color)
        self.query_label.pack(pady=(10, 5))
        self.query_entry = tk.Entry(self)
        self.query_entry.pack(pady=(0, 5))

        # Default search type to "Everything" (more comprehensive)
        self.type_var = tk.IntVar(value=1)
        self.r1 = tk.Radiobutton(self, text="Everything", bg=self.bg_color, fg=self.text_color,
                                 selectcolor="black",
                                 variable=self.type_var, value=1, command=self.update_type)
        self.r1.pack()
        self.r2 = tk.Radiobutton(self, text="Top Headlines", bg=self.bg_color, fg=self.text_color,
                                 selectcolor="black", 
                                 variable=self.type_var, value=2, command=self.update_type)
        self.r2.pack()

        # Set a divider to mark optional parameters
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill=tk.X, padx=30, pady=(20, 0))
        self.optional_label = tk.Label(self, text="Advanced Search:", bg=self.bg_color, fg=self.text_color)
        self.optional_label.pack(pady=(20, 0))

        # Dropdown menus for country and language
        self.country_menu = DropMenu(self, text="Country (Top Headlines only):", options=COUNTRY_OPTIONS)
        self.language_menu = DropMenu(self, text="Language:", options=LANGUAGE_OPTIONS)
        
        for menu in [self.country_menu, self.language_menu]:
            menu.create_label()
            menu.create_menu()

        # Time period entries
        self.time_from_label = tk.Label(self, text="From (YYYY-MM-DD):", bg=self.bg_color, fg=self.text_color)
        self.time_from_label.pack(pady=(10, 5))
        self.time_from_entry = tk.Entry(self)
        self.time_from_entry.pack()

        self.time_to_label = tk.Label(self, text="To (YYYY-MM-DD):", bg=self.bg_color, fg=self.text_color)
        self.time_to_label.pack(pady=(10, 5))
        self.time_to_entry = tk.Entry(self)
        self.time_to_entry.pack()

        # Category options
        self.category_label = tk.Label(self, text="Categories (Top Headlines only):", bg=self.bg_color, fg=self.text_color)
        self.category_label.pack(pady=(10, 5))

        self.create_category_menu()

        # Button to run search
        self.search_button = ttk.Button(self, text='Run Search', style='W.TButton', command=search_callback, state="normal")
        self.search_button.pack(pady=(20, 5))

        # Set a divider to mark end of section
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill=tk.X, padx=30, pady=(20, 0))

    def update_type(self):
        self.news_type = self.type_var.get()

    def create_category_menu(self):
        categories = CATEGORY_OPTIONS
        check_buttons = []
        check_vars = []

        # Create a var (for backend functions) and checkbutton (for user) for each category
        for i in range(len(categories)):
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self, variable=v, text=categories[i].title(), width=15, anchor=tk.W, 
                                bg=self.bg_color, fg=self.text_color, selectcolor='black',
                                command=self.category_callback).pack()
            check_buttons.append(cb)
            check_vars.append(v)

        self.check_buttons = check_buttons
        self.check_vars = check_vars


class articleGroup:
    def __init__(self, root, bg_color, spacing_color, row, url, title, description, author, 
                 source, timestamp, img_url, wrap_len):
        self.root = root
        self.bg_color = bg_color,
        self.spacing_color = spacing_color
        self.row = row
        self.url = url
        self.title = title
        self.description = description
        self.author = author
        self.source = source
        self.timestamp = timestamp
        self.img_url = img_url
        self.wrap_len = wrap_len

        # GUI layout
        if True: # TO-DO: Add option to turn off for speed
            self.create_thumbnail()
            self.wrap_len -= 100

        self.create_news_title()
        self.create_description()
        self.create_author()
        self.create_source()
        self.create_timestamp()

        # Scrape after articles have loaded
        self.create_scrape_row()

        # Formtting space between articles
        self.spacing = tk.Label(self.root, text="", anchor="w", justify="left", bg=self.spacing_color)
        self.spacing.grid(row=self.row+4, column=0, columnspan=4, sticky='nsew')

    def create_thumbnail(self):
        # Download image
        u = requests.get(self.img_url)

        # Convert image
        img = Image.open(io.BytesIO(u.content))
        img = img.resize((128, 128))
        self.img = ImageTk.PhotoImage(img)

        # GUI img label
        self.img_label = tk.Label(self.root, image=self.img, bg=self.bg_color)
        self.img_label.grid(row=self.row, column=0, rowspan=5, sticky='n')
        self.img_label.image = self.img

    def create_news_title(self):
        # Shorten long titles
        if len(self.title) > 100:
            title = self.title[:97] + "..."
        else:
            title = self.title

        # Callback to open link
        def web_callback(url):
            webbrowser.open_new_tab(url)

        # GUI label
        self.title_label = tk.Label(self.root, text=title, anchor="w", justify="left", bg=self.bg_color,
                                    font='Helvetica 10 bold underline', cursor="hand2")
        self.title_label.grid(row=self.row, column=1, columnspan=3, sticky='nsew')
        self.title_label.bind("<ButtonRelease-1>", lambda e: web_callback(self.url))

    def create_description(self):
        # Remove html tags
        pattern = r'<[^>]*>'
        try:
            text = re.sub(pattern, '', self.description)
        except:
            text = self.description

        # GUI label
        self.description_label = tk.Label(self.root, text=text, bg=self.bg_color, anchor="w", justify="left", wraplength=self.wrap_len)
        self.description_label.grid(row=self.row+1, column=1, columnspan=3, sticky='nsew')

    def create_author(self):
        text = f"Author: {self.author}"
        self.author_label = tk.Label(self.root, text=text, bg=self.bg_color, anchor="w", justify="left")
        self.author_label.grid(row=self.row+2, column=1, sticky='nsew')

    def create_source(self):
        self.source_label = tk.Label(self.root, text=self.source, bg=self.bg_color, anchor="w", justify="left")
        self.source_label.grid(row=self.row+2, column=2, sticky='nsew')

    def create_timestamp(self):
        # Format time
        pattern = r'\.\d+Z$'
        ts = re.sub(pattern, '+00:00', self.timestamp)
        try:
            dt = datetime.datetime.fromisoformat(ts)
            ts =  dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.datetime.fromisoformat(ts.split("T")[0])
            ts = dt.strftime("%Y-%m-%d")

        text = f"Published: {ts}"

        # GUI Label
        self.timestamp_label = tk.Label(self.root, text=text, bg=self.bg_color, anchor="w", justify="left")
        self.timestamp_label.grid(row=self.row+2, column=3, sticky='nsew')

    def scrape_content(self):
        # Run scraper module (find ads, scripts and socials with BeautifulSoup)
        url = self.url
        
        scraper = Scraper(url)
        scraper.make_request()
        scraper.count_adverts()
        scraper.count_scripts()
        scraper.get_linked_data()
        scraper.get_socials()

        self.scraped = scraper
        
    def create_scrape_row(self):
        # Get content
        self.scrape_content()
        scraped_content = self.scraped

        # Format Socials
        socials = getattr(scraped_content, 'socials', None)
        socials_text = "Socials: "

        socials = [s for s in socials if s]
        socials = set(socials)
        if len(socials) > 0:
            socials_text += ", ".join(socials)
        self.socials = tk.Label(self.root, text=socials_text, anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.socials.grid(row=self.row+3, column=1, sticky='nsew')

        # Fromat Keywords
        keywords = getattr(scraped_content, 'keywords', None)
        keywords_text = "Keywords: "
        if isinstance(keywords, list):
            keywords = set(keywords)
            keywords_text += ", ".join(keywords)
        elif isinstance(keywords, str):
            keywords_text += keywords

        if len(keywords_text) > 60:
            keywords_text = keywords_text[:57] + "..."

        self.keywords = tk.Label(self.root, text=keywords_text, anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.keywords.grid(row=self.row+3, column=2, sticky='nsew')

        # Format Ad Count
        ads = getattr(scraped_content, 'ad_count', 0)
        self.ads_label = tk.Label(self.root, text=f"Ads: {ads}", anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.ads_label.grid(row=self.row+3, column=3, sticky='nsew')
        self.ads_count = ads


class ContentFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color, width):
        tk.Frame.__init__(self, root, width=width, bg=bg_color)
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.cached = {}
        self.page = None
        self.analytics_content = None
        self.show_content = True
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # # Header
        # self.header_label = tk.Label(self, text="Content View:", bg=bg_color)
        # self.header_label.pack(pady=(10, 5))

        ##### Frames layout (navigation and content)
        self.nav = tk.Frame(self, bg=self.bg_color)
        self.nav.pack(side=tk.TOP)
        self.display = tk.Frame(self, bg=self.bg_color)
        self.display.pack()
        self.end_nav = tk.Frame(self, bg=self.bg_color)
        self.end_nav.pack(side=tk.BOTTOM)

        ##### Navigation
        # Button styles
        style = ttk.Style()
        style.configure('W.TButton', background=self.bg_color, font=('calibri', 10, 'bold', 'underline'))

        # Back button
        self.button_back = ttk.Button(self.root, text='Last Page', style='W.TButton', command=self.back_frame, state="disabled")
        self.button_back.pack(in_=self.nav, side=tk.LEFT, pady=10)

        # Forward button
        analytics_state = "normal"
        if self.root.downloaded_results is None:
            next_state = "disabled"
            analytics_state = "disabled"
        elif len(self.root.downloaded_results) < self.root.page_len:
            next_state = "disabled"
            self.page = 0
        else:
            next_state = "normal"
            self.page = 0
        self.button_next = ttk.Button(self.root, text='Next Page', style='W.TButton', command=self.next_frame, state=next_state)
        self.button_next.pack(in_=self.nav, side=tk.RIGHT, pady=10)

        # Analytics button
        self.button_analytics = ttk.Button(self.root, text="Analytics", style='W.TButton', command=self.show_analytics, state=analytics_state)
        self.button_analytics.pack(in_=self.end_nav)

        ##### Content
        self.wrap_len = width - 100
        self.articles = {}

    def show_results(self):
        # Show only when API download completed
        if self.root.downloaded_results:
            cut_off = min(self.root.page_len, len(self.root.downloaded_results))
            data = self.root.downloaded_results[:cut_off]

            # Set up first page of results
            self.cached[self.page] = tk.Frame(self.root)
            self.add_article_elements(target=self.cached[self.page], articles=data)
            self.cached[self.page].pack(in_=self.display)

    def add_article_elements(self, target, articles):
        # Function to create an inner frame for each article, allowing for grid use within
        counter = 0

        for a in articles:
            if a["title"] != "[Removed]":
                source = a.get('source', None)
                if source:
                    source = source.get('name', None)

                self.articles[counter] = articleGroup(
                    root=target,
                    bg_color="#FFF8E4",
                    spacing_color=self.bg_color,
                    row=5*counter,
                    url=a.get('url', None),
                    title=a.get('title', None),
                    description=a.get('content', None),
                    author=a.get('author', None),
                    source=source,
                    timestamp=a.get('publishedAt', None),
                    img_url=a.get('urlToImage', None),
                    wrap_len=self.wrap_len
                )

                counter +=1

    def next_frame(self):
        # Remove existing
        self.cached[self.page].pack_forget()
        
        # Create new frame if doesn't exist
        self.page += 1

        # Select relevant articles from api request
        start_idx = self.page * self.root.page_len
        end_idx = min(start_idx + self.root.page_len, len(self.root.downloaded_results))
        selected_data = self.root.downloaded_results[start_idx:end_idx]

        # Cache helps performance if images have been loaded
        if self.page not in self.cached.keys():
            self.cached[self.page] = tk.Frame(self.root)
            self.add_article_elements(self.cached[self.page], selected_data)
        
        # Pack next page
        self.cached[self.page].pack(in_=self.display)

        # Disable next button if final article is reached
        self.button_back["state"] = "normal"
        if end_idx == len(self.root.downloaded_results):
            self.button_next["state"] = "disabled"

    def back_frame(self):
        # Dont go below zero
        if self.page != 0:
            # Remove current
            self.cached[self.page].pack_forget()
            
            # Show last
            self.page -= 1
            self.cached[self.page].pack(in_=self.display)
            self.button_next["state"] = "normal"

        # Disable back button if returning to start
        if self.page == 0:
            self.button_back["state"] = "disabled"
            self.button_next["state"] = "normal"

    def extract_date_time(self, timestamp):
        # Timestamps from API results are not always consistent
        pattern = r'\.\d+Z$'
        ts = re.sub(pattern, '+00:00', timestamp)

        try:
            dt = datetime.datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.datetime.fromisoformat(ts.split("T")[0])
            return dt.strftime("%Y-%m-%d")

    def create_thumbnail(self, url):
        # Download article image and shink to thumbnail
        u = requests.get(url)
        img = Image.open(io.BytesIO(u.content))
        img = img.resize((128, 128))
        
        return ImageTk.PhotoImage(img)

    def show_analytics(self):
        if self.show_content:
            self.root.statusbar.set(text="Loading Analytics ...")

            # Remove existing content
            self.cached[self.page].pack_forget()
            self.button_back["state"] = "disabled"
            self.button_next["state"] = "disabled"

            # Create or show new content
            if self.analytics_content is None:
                self.analytics_content = tk.Frame()
                self.analytics_frame = GraphFrame(
                    self.analytics_content, 
                    bg_color="#FFF1C8", 
                    text_color="#000000",
                    data=self.root.downloaded_results,
                    width=800,
                    height=700
                )

            self.analytics_content.pack(in_=self.display)
            self.root.statusbar.clear()
        else:
            # Remove existing content
            self.analytics_content.pack_forget()
            
            # Show new content
            self.cached[self.page].pack(in_=self.display)
            if self.page == 0:
                self.button_back["state"] = "disabled"
            else:
                self.button_back["state"] = "normal"
            
            if (self.page + 1) * self.root.page_len > len(self.root.downloaded_results):
                self.button_next["state"] = "disabled"
            else:
                self.button_next["state"] = "normal"

        # Adjust switching options
        self.show_content = not self.show_content
        text = "Analytics" if self.show_content else "Back to News"
        self.button_analytics.config(text=text)

        
class MainApp:
    # __api_key = ""

    def __init__(self, root):
        self.root = root
        
        width = 1200
        height = 900
        self.root.geometry(f"{width}x{height}+0+0")
        self.root.title("News Aggregator")
        self.root.news = None
        self.root.downloaded_results = None
        self.root.page_len = 5
        
        # Status bar (bottom bar)
        self.root.statusbar = StatusBar(root)
        self.root.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Menu (left frame)
        menu_width = 200
        self.left_frame = MenuFrame(root, bg_color="#27212E", text_color="#FFFFFF", width=menu_width,
                                    category_callback=self.update_category_selections,
                                    search_callback=self.search_news)
        self.left_frame.pack_propagate(False)
        # self.left_frame.key_entry.bind("<Return>", self.set_api_key)

        # Content (right frame)
        content_width = width - menu_width
        
        self.right_frame = ContentFrame(root, bg_color="#FFF1C8", text_color="#000000", width=content_width)
        self.right_frame.pack_propagate(False)

    # # API Key stored as private variable instead of requiring user input every load
    # def set_api_key(self, event):
    #     MainApp.__api_key = self.left_frame.key_entry.get()
    #     self.left_frame.key_entry.delete(0, tk.END)

    def update_category_selections(self):
        options = [var.get() for var in self.left_frame.check_vars]

        if all(options):
            self.left_frame.selected_categories = None
        else:
            selected_categories = [category for category, selected in zip(CATEGORY_OPTIONS, options) if selected]
            self.left_frame.selected_categories = selected_categories
        
    def params_check(self):
        # Check which params are entered
        params = {}

        query_content = self.left_frame.query_entry.get()
        if query_content:
            params["q"] = self.left_frame.query_entry.get()
        
        language = self.left_frame.language_menu.option_var.get()
        if language:
            params["language"] = language
        
        country = self.left_frame.country_menu.option_var.get()
        if country:
            params["country"] = country

        time_from = self.left_frame.time_from_entry.get()
        time_to = self.left_frame.time_to_entry.get()

        if time_from:
            params["from"] = time_from
            
        if time_to:
            params["to"] = time_to

        if self.left_frame.selected_categories:
            categories_str = ",".join(self.left_frame.selected_categories)
            params["category"] = categories_str
            
        return params

    def search_news(self):
        # Function to run when search button is clicked
        self.root.statusbar.set(text="Downloading from NewsAPI ...")

        # Clear existing data
        self.reset_content()

        # Create news object
        if self.left_frame.news_type == 2:
            news_obj = TopHeadlines()
        else:
            news_obj = News()
        
        # Add params
        params = self.params_check()
        
        if len(params) > 0:
            # Run NewsAPI functions
            news_obj.add_params(params)
            self.news = news_obj
            results = news_obj.make_request()

            if results.get("status", None) == "ok":
                i = results["totalResults"] # Placeholder if pages function is added
                
                # Remove invalid articles and cache
                articles = [a for a in results["articles"] if a["source"]["name"] != "[Removed]"]
                self.root.downloaded_results = articles

                # Show number of results in status text
                j = len(articles)
                status_text = f"Retrieved {j} results. "

                # Show first parge of results
                self.right_frame.page = 0
                self.right_frame.show_results()
                self.right_frame.button_analytics["state"] = "normal"

                # Activate "Next" button only if enough articles are available
                if len(self.root.downloaded_results) > self.root.page_len:
                    self.right_frame.button_next["state"] = "normal"

                # Check if any warnings from News API
                if news_obj.removed_params:
                    remove_warning = "Removed params: " + "".join(news_obj.removed_params)
                    status_text += remove_warning

                if news_obj.warnings:
                    status_text += "".join(news_obj.warnings)

                # Update status bar
                self.root.statusbar.set(text=status_text)
            else:
                # Show error if API requested but error returned
                messagebox.showerror("Error", "API could not be accessed. ")
                status_text = results.get("message", "Error with API, please try again. ")
                self.root.statusbar.set(text=status_text)
        else:
            # Show warning message if no valid parameters pass UI checks
            if self.left_frame.news_type == 2:
                status_text = "No valid search parameters entered. Try another search query, language, or country. " 
            else:
                status_text = "No valid search parameters entered. Try another search query. " 
                
            messagebox.showwarning("Warning", "No valid search terms entered, try again. ")
            self.root.statusbar.set(text=status_text)

    def reset_content(self):
        # Clear results
        self.root.downloaded_results = None
        
        # Disable navigation buttons
        self.right_frame.button_next["state"] = "disabled"
        self.right_frame.button_back["state"] = "disabled"
        self.right_frame.button_analytics["state"] = "disabled"
        self.right_frame.button_analytics.config(text="Analytics")

        # Unpack currently displayed content 
        if self.right_frame.show_content:
            if self.right_frame.page:
                self.right_frame.cached[self.right_frame.page].pack_forget()
        else:
            self.right_frame.analytics_content.pack_forget()

        self.right_frame.analytics_content = None
        self.right_frame.show_content = True

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
