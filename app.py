import tkinter as tk
import datetime
import io
import re
import requests
import webbrowser

from tkinter import ttk
from newsapi import News, TopHeadlines
from PIL import ImageTk, Image

COUNTRY_OPTIONS = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                   'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
                   'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
                    'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']
LANGUAGE_OPTIONS = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh']
CATEGORY_OPTIONS = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

TEST_ARTICLES = [
            {'source': {'id': None, 'name': '[Removed]'}, 'author': None, 'title': '[Removed]', 'description': '[Removed]', 'url': 'https://removed.com', 'urlToImage': None, 'publishedAt': '1970-01-01T00:00:00Z', 'content': '[Removed]'}, 
            {'source': {'id': 'bbc-sport', 'name': 'BBC Sport'}, 'author': None, 'title': 'NBA play-offs: Tyrese Haliburton leads Indiana Pacers to win over Milwaukee Bucks', 'description': 'Tyrese Haliburton converts a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series.', 'url': 'http://www.bbc.co.uk/sport/basketball/articles/cg30zl29mzlo', 'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_sport/7f48/live/1c411940-045e-11ef-b9d8-4f52aebe147d.jpg', 'publishedAt': '2024-04-27T07:52:13.3513784Z', 'content': 'Tyrese Haliburton converted a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series… [+864 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Cleveland Cavaliers vs. Orlando Magic NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Find out how and when to watch Game 4 of the Cavaliers vs. Magic NBA Playoffs series, even if you don't have cable.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-cavaliers-vs-magic-nba-playoffs-game-game-4-livestream-options-start-time-and-more/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/6570261c-23f8-4c32-8417-2cfd5148e080/thumbnail/1200x630/98546cb5680e0d153001f7a7148851d3/gettyimages-2150246951-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T05:06:47+00:00', 'content': 'Darius Garland #10 of the Cleveland Cavaliers dribbles the ball against Paolo Banchero #5 of the Orlando Magic during the third quarter of game three of the Eastern Conference First Round Playoffs at… [+8406 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Here's how and when to watch Game 4 of the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-denver-nuggets-vs-los-angeles-lakers-game-4/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/0d01dd18-1c25-4fcb-9c8d-1b080342a800/thumbnail/1200x630/3d5ceb8e0d7954dbedd2664d016fbfbf/gettyimages-2150339085-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:59:00+00:00', 'content': 'Nikola Jokic #15 of the Denver Nuggets during game three of the Western Conference First Round Playoffs at Crypto.com Arena on April 25, 2024 in Los Angeles, California.\r\nRonald Martinez/Getty Images… [+10776 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Boston Celtics vs. Miami Heat NBA Playoffs game tonight: Game 3 livestream options, start time, more', 'description': "Game 3 of the Celtics vs. Heat NBA Playoffs series is can't-miss basketball. Here's how and when to watch tonight.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-boston-celtics-vs-miami-heat-nba-playoffs-game-3/', 'urlToImage': 'https://assets1.cbsnewsstatic.com/hub/i/r/2024/04/26/09ef6820-2df5-4120-96f9-5d8884a6543e/thumbnail/1200x630/6d15d84003a1d8c8726ff8e1dfb5501b/gettyimages-2149460985-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:47:00+00:00', 'content': 'Tyler Herro #14 of the Miami Heat looks at his bench after making a three-point basket against the Boston Celtics during the second quarter of game two of the Eastern Conference First Round Playoffs … [+8404 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the OKC Thunder vs. New Orleans Pelicans NBA Playoffs game tonight: Game 3 livestream options, more', 'description': "Here's how and when to watch Game 3 of the OKC Thunder vs. New Orleans Pelicans NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-okc-thunder-vs-new-orleans-pelicans-nba-playoffs-game-3/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/85e98138-3298-4ec7-a1a7-e5030b12aa2d/thumbnail/1200x630/a5861ab2092c404f418cfb7687dd2d1c/gettyimages-2150073262-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:10:19+00:00', 'content': 'Oklahoma City Thunder players react from the bench after a three-pointer during game two of the first round of the NBA playoffs against the New Orleans Pelicans at Paycom Center on April 24, 2024 in … [+8574 chars]'}, 
            {'source': {'id': 'abc-news-au', 'name': 'ABC News (AU)'}, 'author': 'ABC News', 'title': "Joel Embiid fights Bell's palsy to drop NBA playoff career high as Sixers down Knicks", 'description': 'Philadelphia 76ers star Joel Embiid went to the doctors complaining of a migraine prior to the playoffs, only for the diagnosis to be something more sinister that impacts how he looks on the court.', 'url': 'https://www.abc.net.au/news/2024-04-26/nba-playoffs-joel-embiid-bells-palsy-sixers-knicks-game-3/103773714', 'urlToImage': 'https://live-production.wcms.abc-cdn.net.au/d8406c6fa93bfc53f1dd55f9976d5d2a?impolicy=wcms_watermark_news&cropH=2531&cropW=4500&xPos=0&yPos=338&width=862&height=485&imformat=generic', 'publishedAt': '2024-04-26T05:28:24Z', 'content': "<ul><li>In short:\xa0Joel Embiid has been diagnosed with Bell's palsy, a form of facial paralysis, after initially complaining of migraines prior to the NBA playoffs.</li><li>Embiid battled through the … [+2061 chars]"},
        ]

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
        self.option_var = tk.StringVar()
        self.option_var.set(self.options[0])

        self.menu = ttk.Combobox(self.root, width=self.width, textvariable=self.option_var, values=self.options)
        self.menu.pack()

class MenuFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color, update_callback):
        self.bg_color = bg_color
        self.text_color = text_color
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


class articleGroup:
    def __init__(self, root, row, url, title, description, author, source, timestamp, img_url, wrap_len):
        self.root = root
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
        # self.create_thumbnail()
        self.create_news_title()
        self.create_description()
        self.create_author()
        self.create_source()
        self.create_timestamp()

    def create_thumbnail(self):
        # Download image
        u = requests.get(self.img_url)

        # Convert image
        img = Image.open(io.BytesIO(u.content))
        img = img.resize((128, 128))
        self.img = ImageTk.PhotoImage(img)

        # GUI img label
        self.img_label = tk.Label(self.root, image=self.img)
        self.img_label.grid(row=self.row, column=0, rowspan=3, sticky='nsew')
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
        self.title_label = tk.Label(self.root, text=title, anchor="w", justify="left",
                                    font='Helvetica 10 bold underline', cursor="hand2")
        self.title_label.grid(row=self.row, column=1, columnspan=3, sticky='nsew', pady=(5, 0))
        self.title_label.bind("<ButtonRelease-1>", lambda e: web_callback(self.url))

    def create_description(self):
        # Remove html tags
        pattern = r'<[^>]*>'
        text = re.sub(pattern, '', self.description)

        # GUI label
        self.description_label = tk.Label(self.root, text=text, anchor="w", justify="left", wraplength=self.wrap_len)
        self.description_label.grid(row=self.row+1, column=1, columnspan=3, sticky='nsew')

    def create_author(self):
        text = f"Author: {self.author}"
        self.author_label = tk.Label(self.root, text=text, anchor="w", justify="left")
        self.author_label.grid(row=self.row+2, column=1, sticky='nsew')

    def create_source(self):
        self.source_label = tk.Label(self.root, text=self.source, anchor="w", justify="left")
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
        self.timestamp_label = tk.Label(self.root, text=text, anchor="w", justify="left")
        self.timestamp_label.grid(row=self.row+2, column=3, sticky='nsew')


class ContentFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.cached = {}
        self.page = 0
        tk.Frame.__init__(self, root, width=800, highlightbackground="black", highlightthickness=1, bg=bg_color)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        self.header_label = tk.Label(self, text="Content View:", bg=bg_color)
        self.header_label.pack(pady=(10, 5))

        ##### Frames layout
        self.nav = tk.Frame(self, bg=self.bg_color)
        self.nav.pack(side=tk.TOP)
        self.display = tk.Frame(self, bg=self.bg_color)
        self.display.pack()

        ##### Navigation
        # Button styles
        style = ttk.Style()
        style.configure('W.TButton', background=self.bg_color, font=('calibri', 10, 'bold', 'underline'))

        # Back button
        self.button_back = ttk.Button(self.root, text='Last Page', style='W.TButton', command=self.back_frame, state="disabled")
        self.button_back.pack(in_=self.nav, side=tk.LEFT, pady=10)

        # Forward button
        self.button_next = ttk.Button(self.root, text='Next Page', style='W.TButton', command=self.next_frame, state="normal")
        self.button_next.pack(in_=self.nav, side=tk.RIGHT, pady=10)

        ##### Content
        self.wrap_len = 700
        self.articles = {}

        self.cached[self.page] = tk.Frame(self.root)
        self.add_article_elements(target=self.cached[self.page], articles=TEST_ARTICLES)
        self.cached[self.page].pack(in_=self.display)

    def add_article_elements(self, target, articles):
        counter = 0

        for a in articles:
            if a["title"] != "[Removed]":
                source = a.get('source', None)
                if source:
                    source = source.get('name', None)

                self.articles[counter] = articleGroup(
                    #root=self.content_frame,
                    root=target,
                    row=3*counter,
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
        if self.page not in self.cached.keys():
            self.cached[self.page] = tk.Frame(self.root)
            self.add_article_elements(self.cached[self.page], TEST_ARTICLES[::-1])
        
        # Pack next page
        self.cached[self.page].pack(in_=self.display)

        self.button_back["state"] = "normal"
        if self.page == 1:
            self.button_next["state"] = "disabled"

    def back_frame(self):
        # Dont go below zero
        if self.page != 0:
            # Remove current
            self.cached[self.page].pack_forget()
            
            # Show last
            self.page -= 1
            self.cached[self.page].pack(in_=self.display)
        
        if self.page == 0:
            self.button_back["state"] = "disabled"
            self.button_next["state"] = "normal"

    def extract_date_time(self, timestamp):
        pattern = r'\.\d+Z$'
        ts = re.sub(pattern, '+00:00', timestamp)

        try:
            dt = datetime.datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.datetime.fromisoformat(ts.split("T")[0])
            return dt.strftime("%Y-%m-%d")

    def create_thumbnail(self, url):
        u = requests.get(url)
        img = Image.open(io.BytesIO(u.content))
        img = img.resize((128, 128))
        
        return ImageTk.PhotoImage(img)


class MainApp:
    __api_key = ""

    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")
        self.root.title("News Aggregator")
        self.news = None
        self.cached_results = None

        # Menu
        self.left_frame = MenuFrame(root, bg_color="#27212E", text_color="#FFFFFF", 
                                    update_callback=self.update_category_selections)
        self.left_frame.pack_propagate(False)
        self.left_frame.key_entry.bind("<Return>", self.set_api_key)

        # API Button
        self.left_frame.call_button = tk.Button(self.left_frame, text="Get News!", command=self.fetch_news)
        self.left_frame.call_button.pack(pady=(20, 5))

        # Content
        self.right_frame = ContentFrame(root, bg_color="#FFF1C8", text_color="#000000")
        self.right_frame.pack_propagate(False)

        if self.cached_results:
            self.display_results()
            
        # # Show selections
        # self.category_label = tk.Label(self.right_frame, text="")
        # self.update_category_selections()
        # self.category_label.pack()

        # # Display country/Language
        # var = self.left_frame.country_menu.option_var.get()
        # self.country_label = tk.Label(self.right_frame, text=f"Country: {var}")
        # self.country_label.pack()
        # self.left_frame.country_menu.menu.bind('<<ComboboxSelected>>', self.update_combobox_selection)
        
        # var = self.left_frame.language_menu.option_var.get()
        # self.language_label = tk.Label(self.right_frame, text=f"Language: {var}")
        # self.language_label.pack()
        # self.left_frame.language_menu.menu.bind('<<ComboboxSelected>>', self.update_combobox_selection)

    def set_api_key(self, event):
        MainApp.__api_key = self.left_frame.key_entry.get()
        self.left_frame.key_entry.delete(0, tk.END)

    def update_category_selections(self):
        options = [str(var.get()) for var in self.left_frame.check_vars if var.get()]
        self.category_label.config(text="Selected options: " + ", ".join(options))
    
    def update_combobox_selection(self, event):
        country_var = self.left_frame.country_menu.option_var.get()
        self.country_label.config(text=f"Country: {country_var}")

        language_var = self.left_frame.language_menu.option_var.get()
        self.language_label.config(text=f"Language: {language_var}")

    def fetch_news(self):
        news_obj = TopHeadlines()
        
        # Add params
        params = {}
        if self.left_frame.query_entry != "":
            params["q"] = self.left_frame.query_entry.get()

        if len(params) > 0:
            news_obj.add_params(params)
            self.news = news_obj
            # self.cached_results = news_obj.make_request()
            
            self.display_results()

    def display_results(self):
        self.display = {}
        self.image = {}
        self.text = {}
        count = 0

        #for article in self.cached_results["articles"][:10]:
        articles = [
            {'source': {'id': None, 'name': '[Removed]'}, 'author': None, 'title': '[Removed]', 'description': '[Removed]', 'url': 'https://removed.com', 'urlToImage': None, 'publishedAt': '1970-01-01T00:00:00Z', 'content': '[Removed]'}, 
            {'source': {'id': 'bbc-sport', 'name': 'BBC Sport'}, 'author': None, 'title': 'NBA play-offs: Tyrese Haliburton leads Indiana Pacers to win over Milwaukee Bucks', 'description': 'Tyrese Haliburton converts a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series.', 'url': 'http://www.bbc.co.uk/sport/basketball/articles/cg30zl29mzlo', 'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_sport/7f48/live/1c411940-045e-11ef-b9d8-4f52aebe147d.jpg', 'publishedAt': '2024-04-27T07:52:13.3513784Z', 'content': 'Tyrese Haliburton converted a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series… [+864 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Cleveland Cavaliers vs. Orlando Magic NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Find out how and when to watch Game 4 of the Cavaliers vs. Magic NBA Playoffs series, even if you don't have cable.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-cavaliers-vs-magic-nba-playoffs-game-game-4-livestream-options-start-time-and-more/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/6570261c-23f8-4c32-8417-2cfd5148e080/thumbnail/1200x630/98546cb5680e0d153001f7a7148851d3/gettyimages-2150246951-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T05:06:47+00:00', 'content': 'Darius Garland #10 of the Cleveland Cavaliers dribbles the ball against Paolo Banchero #5 of the Orlando Magic during the third quarter of game three of the Eastern Conference First Round Playoffs at… [+8406 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Here's how and when to watch Game 4 of the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-denver-nuggets-vs-los-angeles-lakers-game-4/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/0d01dd18-1c25-4fcb-9c8d-1b080342a800/thumbnail/1200x630/3d5ceb8e0d7954dbedd2664d016fbfbf/gettyimages-2150339085-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:59:00+00:00', 'content': 'Nikola Jokic #15 of the Denver Nuggets during game three of the Western Conference First Round Playoffs at Crypto.com Arena on April 25, 2024 in Los Angeles, California.\r\nRonald Martinez/Getty Images… [+10776 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Boston Celtics vs. Miami Heat NBA Playoffs game tonight: Game 3 livestream options, start time, more', 'description': "Game 3 of the Celtics vs. Heat NBA Playoffs series is can't-miss basketball. Here's how and when to watch tonight.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-boston-celtics-vs-miami-heat-nba-playoffs-game-3/', 'urlToImage': 'https://assets1.cbsnewsstatic.com/hub/i/r/2024/04/26/09ef6820-2df5-4120-96f9-5d8884a6543e/thumbnail/1200x630/6d15d84003a1d8c8726ff8e1dfb5501b/gettyimages-2149460985-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:47:00+00:00', 'content': 'Tyler Herro #14 of the Miami Heat looks at his bench after making a three-point basket against the Boston Celtics during the second quarter of game two of the Eastern Conference First Round Playoffs … [+8404 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the OKC Thunder vs. New Orleans Pelicans NBA Playoffs game tonight: Game 3 livestream options, more', 'description': "Here's how and when to watch Game 3 of the OKC Thunder vs. New Orleans Pelicans NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-okc-thunder-vs-new-orleans-pelicans-nba-playoffs-game-3/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/85e98138-3298-4ec7-a1a7-e5030b12aa2d/thumbnail/1200x630/a5861ab2092c404f418cfb7687dd2d1c/gettyimages-2150073262-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:10:19+00:00', 'content': 'Oklahoma City Thunder players react from the bench after a three-pointer during game two of the first round of the NBA playoffs against the New Orleans Pelicans at Paycom Center on April 24, 2024 in … [+8574 chars]'}, 
            {'source': {'id': 'abc-news-au', 'name': 'ABC News (AU)'}, 'author': 'ABC News', 'title': "Joel Embiid fights Bell's palsy to drop NBA playoff career high as Sixers down Knicks", 'description': 'Philadelphia 76ers star Joel Embiid went to the doctors complaining of a migraine prior to the playoffs, only for the diagnosis to be something more sinister that impacts how he looks on the court.', 'url': 'https://www.abc.net.au/news/2024-04-26/nba-playoffs-joel-embiid-bells-palsy-sixers-knicks-game-3/103773714', 'urlToImage': 'https://live-production.wcms.abc-cdn.net.au/d8406c6fa93bfc53f1dd55f9976d5d2a?impolicy=wcms_watermark_news&cropH=2531&cropW=4500&xPos=0&yPos=338&width=862&height=485&imformat=generic', 'publishedAt': '2024-04-26T05:28:24Z', 'content': "<ul><li>In short:\xa0Joel Embiid has been diagnosed with Bell's palsy, a form of facial paralysis, after initially complaining of migraines prior to the NBA playoffs.</li><li>Embiid battled through the … [+2061 chars]"},
        ]
        for article in articles:
            if article['source']['name'] != '[Removed]':

                url = article.get("urlToImage", None)
                u = requests.get(url)
                img = Image.open(io.BytesIO(u.content))
                img = img.resize((128, 128))
                self.image[f"article_{count}"] = ImageTk.PhotoImage(img)

                # with urlopen(url) as u:
                #     raw_data = u.content
                #     image = Image.open(io.BytesIO(raw_data))
                #     img = ImageTk.PhotoImage(image)

                self.display[f"article_{count}"] = tk.Label(
                    self.right_frame,
                    # text=article.get("urlToImage", None),
                    image=self.image[f"article_{count}"],
                    width=100,
                    height=100,
                    anchor="w",
                    # justify="left",
                    # width=100,
                    # wraplength=700
                )
                self.display[f"article_{count}"].pack(side=tk.LEFT, pady=(10, 5))
                self.text[f"article_{count}"] = tk.Label(
                    self.right_frame,
                    text=article.get("title", None),
                    width=100,
                    # justify="left",
                    # width=100,
                    # wraplength=700
                )
                self.text[f"article_{count}"].pack(side=tk.RIGHT)

                #self.display[f"article_{count}"].config(image=image, width=image.width(), height=image.height())
                count += 1

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
