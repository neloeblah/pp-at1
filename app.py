import tkinter as tk
import datetime
import os
import io
import re
import requests
import webbrowser
import plotly.express as px
import pandas as pd

from tkinter import ttk
from PIL import ImageTk, Image

from newsapi import News, TopHeadlines
from scraper import Scraper

COUNTRY_OPTIONS = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                   'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
                   'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
                    'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']
LANGUAGE_OPTIONS = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh']
CATEGORY_OPTIONS = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

class StatusBar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.label = tk.Label(self, anchor=tk.E)
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set(self, text):
        self.label.config(text=text)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


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
    def __init__(self, root, bg_color, text_color, width, category_callback, search_callback, latest_callback):
        tk.Frame.__init__(self, root, width=width, bg=bg_color)
        self.bg_color = bg_color
        self.text_color = text_color
        self.category_callback = category_callback
        self.search_callback = search_callback
        self.latest_callback = latest_callback
        self.news_type = 1
        self.selected_categories = None
        self.filter_country = None
        self.filter_language = None 
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Stylings for widgets
        style = ttk.Style()
        style.configure('W.TButton', background="#27212E", font=('Calibri', 12, 'bold'))
        header_font = ("TkDefaultFont", 10, "underline")

        # # Buttons to get latest news
        # self.simple_label = tk.Label(self, text="Simple Search:", bg=self.bg_color, fg=self.text_color, font=header_font)
        # self.simple_label.pack(pady=(20, 5))
        # self.latest_button = ttk.Button(self, text='Get Latest News', style='W.TButton', command=latest_callback, state="disabled")
        # self.latest_button.pack(pady=(10, 5))

        # # Set a divider between two types of seach
        # separator = ttk.Separator(self, orient='horizontal')
        # separator.pack(fill=tk.X, padx=30, pady=(20, 5))

        # Search Query
        # self.advanced_label = tk.Label(self, text="Advanced Search:", bg=self.bg_color, fg=self.text_color, font=header_font)
        # self.advanced_label.pack(pady=(20, 5))
        self.query_label = tk.Label(self, text="Search query:", bg=self.bg_color, fg=self.text_color)
        self.query_label.pack(pady=(10, 5))
        self.query_entry = tk.Entry(self)
        self.query_entry.pack()

        # Search type
        self.type_label = tk.Label(self, text="Search Type:", bg=self.bg_color, fg=self.text_color)
        self.type_label.pack(pady=(20, 5))
        self.type_var = tk.IntVar(value=1)
        self.r1 = tk.Radiobutton(self, text="Everything", bg=self.bg_color, fg=self.text_color,
                                 selectcolor="black",
                                 variable=self.type_var, value=1, command=self.update_type)
        self.r1.pack()
        self.r2 = tk.Radiobutton(self, text="Top Headlines", bg=self.bg_color, fg=self.text_color,
                                 selectcolor="black", 
                                 variable=self.type_var, value=2, command=self.update_type)
        self.r2.pack()

        # Dropdown menus for country and language
        self.country_menu = DropMenu(self, text="Country (optional):", options=COUNTRY_OPTIONS)
        self.language_menu = DropMenu(self, text="Language (Top Headlines only):", options=LANGUAGE_OPTIONS)
        
        for menu in [self.country_menu, self.language_menu]:
            menu.create_label()
            menu.create_menu()

        # Run search version of news
        self.search_button = ttk.Button(self, text='Run Search', style='W.TButton', command=search_callback, state="normal")
        self.search_button.pack(pady=(20, 5))

        # Category options
        self.category_label = tk.Label(self, text="Filter Categories:", bg=self.bg_color, fg=self.text_color)
        self.category_label.pack(pady=(20, 5))

        self.create_category_menu()

        self.test_button = ttk.Button(self, text='Test', style='W.TButton', command=self.test_updates, state="normal")
        self.test_button.pack(pady=(20, 5))

    def update_type(self):
        self.news_type = self.type_var.get()

    def test_updates(self):
        language = self.language_menu.option_var.get()
        if language:
            print(f"add param {language}")

        country = self.country_menu.option_var.get()
        if country:
            print(f"add param {country}")

    def create_category_menu(self):
        categories = CATEGORY_OPTIONS
        check_buttons = []
        check_vars = []

        for i in range(len(categories)):
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self, variable=v, text=categories[i].title(), width=15, anchor=tk.W, 
                                bg=self.bg_color, fg=self.text_color, selectcolor='black',
                                command=self.category_callback).pack()
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
        self.country_var = country_var

    def create_language_menu(self):
        self.language_label = tk.Label(self, text="Select Language:", bg=self.bg_color, fg=self.text_color)
        self.language_label.pack(pady=(20, 5))

        options = [""] + LANGUAGE_OPTIONS

        language_var = tk.StringVar()
        language_var.set(options[0])

        self.language_menu = ttk.Combobox(self, width=5, textvariable=language_var, values=options)
        self.language_menu.pack()
        self.language_var = language_var


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
        # self.create_thumbnail()
        self.create_news_title()
        self.create_description()
        self.create_author()
        self.create_source()
        self.create_timestamp()

        self.create_scrape_row()

        # Formtting
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
        self.img_label.grid(row=self.row, column=0, rowspan=5, sticky='nsew')
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

    def scrape_content(self):
        url = self.url
        
        scraper = Scraper(url)
        scraper.make_request()
        scraper.count_adverts()
        scraper.count_scripts()
        scraper.get_linked_data()
        scraper.get_socials()

        self.scraped = scraper

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

    def create_scrape_row(self):
        # Get content
        self.scrape_content()

        scraped_content = self.scraped

        # Socials
        socials = getattr(scraped_content, 'socials', None)
        socials_text = "Socials: "

        socials = [s for s in socials if s]
        if len(socials) > 0:
            socials_text += ", ".join(socials)
        self.socials = tk.Label(self.root, text=socials_text, anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.socials.grid(row=self.row+3, column=1, sticky='nsew')

        # Keywords
        keywords = getattr(scraped_content, 'keywords', None)
        keywords_text = "Keywords: "
        if isinstance(keywords, list):
            keywords_text += ", ".join(keywords)
        elif isinstance(keywords, str):
            keywords_text += keywords
        self.keywords = tk.Label(self.root, text=keywords_text, anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.keywords.grid(row=self.row+3, column=2, sticky='nsew')

        # Keywords
        ads = getattr(scraped_content, 'ad_count', 0)
        self.ads_label = tk.Label(self.root, text=f"Ads: {ads}", anchor=tk.W, justify=tk.LEFT, bg=self.bg_color)
        self.ads_label.grid(row=self.row+3, column=3, sticky='nsew')
        self.ads_count = ads

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


class GraphFrame():
    def __init__(self, root, bg_color, text_color, data):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.stats = None
        self.stats_count = None
        self.stats_len = None
        self.plots = {}
        self.labels = {}

        # Create subfolder if required
        if not os.path.exists("images"):
            os.mkdir("images")
        else:
            # Clear existing files 
            for f in os.listdir("images"):
                os.remove(f"images/{f}")
        
        # Data wrangling
        self.summarise_data(data)

        # Create plots and save pngs
        self.create_vbar_plot(
            df=self.stats_count,
            x="Count", y="Source",
            mean=self.stats.groupby("Source")["Length"].count().mean(),
            name="fig_source_count.png"
        )
        self.create_vbar_plot(
            df=self.stats_len,
            x="Length", y="Source",
            mean=self.stats["Length"].mean(),
            name="fig_source_length.png"
        )
        self.create_line_plot()

        # Display plots
        filenames = ["fig_source_count.png", "fig_source_length.png", "fig_published_at.png"]
        for i, filename in enumerate(filenames):
            self.display_plot(filename, counter=i)

    def summarise_data(self, data):
        stats = []
        for article in data:
            # Get source name and article length
            source = article["source"]["name"]
            length = self.get_article_length(article.get('content', ''))
            published = article.get("publishedAt", None)

            stats.append([source, length, published])

        # Store stats
        df = pd.DataFrame(stats, columns=["Source", "Length", "Published"])
        self.stats = df

        # Run other aggregations 
        self.summarise_counts()
        self.summarise_lengths()

    def summarise_counts(self):
        # Get counts by soure
        df = self.stats.groupby("Source", as_index=False)["Length"].count()
        df.columns = ["Source", "Count"]

        # Mark top 10
        df.sort_values("Source", inplace=True)
        df["Rank"] = df["Count"].rank(method="first")
        df["Top"] = True
        df.loc[df["Rank"] >= 10, "Top"] = False

        # Group smaller names into "Other" bucket to save room on graphs
        df.loc[~df["Top"], "Source"] = "Other"
        df = df.groupby("Source", as_index=False)["Count"].sum()
        df.sort_values("Count", ascending=False, inplace=True)
        self.stats_count = df

    def summarise_lengths(self):
        df = self.stats.copy()
        
        # Mark top 10
        sources = self.stats_count["Source"].tolist()
        df["Top"] = True
        df.loc[~df["Source"].isin(sources), "Top"] = False
        df.loc[~df["Top"], "Source"] = "Other"

        # Get average article length per source
        df = df.groupby("Source", as_index=False)["Length"].mean()
        df.sort_values("Length", ascending=False, inplace=True)

        self.stats_len = df

    def get_article_length(self, content):
        # Find char counter at end of content
        pattern = r"\[\+\d+\s+\w+\]"

        p = re.compile(pattern)
        try:
            match = p.search(content)
        except:
            match = None

        if match:
            # Extract number from char counter
            extra_tag = match.group(0)
            extra_count = re.findall(r"\d+", extra_tag)
            extra_count = int(extra_count[0])

            # Count string portion of content
            stripped_content = content.replace(extra_tag, "")    
            stripped_content = re.sub(r"\u2026", '', stripped_content)
            content_count = len(stripped_content)

        else:
            extra_count = 0
            try:
                content_count = len(content)
            except:
                content_count = 0

        return content_count + extra_count
    
    def create_vbar_plot(self, df, x, y, mean, name):
        # Create color map
        color_map = {source: "#018ADA" for source in df["Source"].unique()}
        color_map["Other"] = "#A5A4AC"

        # Plot
        fig = px.bar(df, x=x, y=y, color=y, orientation="h", 
                    color_discrete_map=color_map,
                    width=400, height=300, template="plotly_dark")
        
        # Formatting
        # Mean should be weighted average across all before the top 10 splits
        fig.add_vline(x=mean, line_color="#9D0620", line_dash="dot")
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        fig.write_image(f"images/{name}")

    def create_line_plot(self):
        df = self.stats.copy()
        df = df.loc[df["Source"] != '[Removed]']
        df = df.loc[df["Published"].notnull()]

        df["Published"] = pd.to_datetime(df['Published'], format='mixed')
        df["Date"] = df['Published'].dt.date
        df = df.groupby('Date', as_index=False)["Length"].count()
        
        fig = px.line(df, x='Date', y='Length', 
                      labels={'Date': 'Date', 'Length': 'Articles'}, 
                      width=800, height=300, template='plotly_dark')
        
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        fig.write_image("images/fig_published_at.png")

    def display_plot(self, filename, counter):
        if os.path.isfile(f"images/{filename}"):
            # Load image
            img = Image.open(f"images/{filename}")
            self.plots[counter] = ImageTk.PhotoImage(img)

            # GUI img label
            row = counter // 2
            col = counter % 2
            colspan = 2 if counter == 2 else 1
            self.labels[counter] = tk.Label(self.root, image=self.plots[counter], bg=self.bg_color)
            self.labels[counter].grid(row=row, column=col, columnspan=colspan, sticky='nsew')
            self.labels[counter].image = self.plots[counter]


class ContentFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color, width):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.cached = {}
        self.page = None
        self.analytics_content = None
        self.show_content = True
        tk.Frame.__init__(self, root, width=width, bg=bg_color)
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
        self.button_analytics.pack(in_=self.display, side=tk.BOTTOM, pady=10)

        ##### Content
        self.wrap_len = width - 100
        self.articles = {}

    def show_results(self):
        if self.root.downloaded_results:
            cut_off = min(self.root.page_len, len(self.root.downloaded_results))
            data = self.root.downloaded_results[:cut_off]

            # Set up first set of results
            self.cached[self.page] = tk.Frame(self.root)
            self.add_article_elements(target=self.cached[self.page], articles=data)
            self.cached[self.page].pack(in_=self.display)

    def add_article_elements(self, target, articles):
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
                    data=self.root.downloaded_results
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
    __api_key = ""

    def __init__(self, root):
        self.root = root
        
        width = 1200
        height = 830
        self.root.geometry(f"{width}x{height}+0+0")
        self.root.title("News Aggregator")
        self.root.news = None
        self.root.downloaded_results = None
        self.root.page_len = 5

        self.root.statusbar = StatusBar(root)
        self.root.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Menu
        menu_width = 200
        self.left_frame = MenuFrame(root, bg_color="#27212E", text_color="#FFFFFF", width=menu_width,
                                    category_callback=self.update_category_selections,
                                    search_callback=self.search_news,
                                    latest_callback=self.latest_news)
        self.left_frame.pack_propagate(False)
        # self.left_frame.key_entry.bind("<Return>", self.set_api_key)

        # Content
        content_width = width - menu_width
        self.right_frame = ContentFrame(root, bg_color="#FFF1C8", text_color="#000000", width=content_width)
        self.right_frame.pack_propagate(False)

    def set_api_key(self, event):
        MainApp.__api_key = self.left_frame.key_entry.get()
        self.left_frame.key_entry.delete(0, tk.END)

    def update_category_selections(self):
        options = [var.get() for var in self.left_frame.check_vars]

        if all(options):
            self.left_frame.selected_categories = None
        else:
            selected_categories = [category for category, selected in zip(CATEGORY_OPTIONS, options) if selected]
            self.left_frame.selected_categories = selected_categories

    def update_combobox_selection(self, event):
        country_var = self.left_frame.country_menu.option_var.get()
        # self.country_label.config(text=f"Country: {country_var}")

        language_var = self.left_frame.language_menu.option_var.get()
        # self.language_label.config(text=f"Language: {language_var}")

    def latest_news(self):
        self.root.statusbar.set(text="Downloading from NewsAPI ...")

        # Clear existing data
        self.reset_content()

        # Create news object
        news_obj = News()

        params = {}

    # TO-DO: update params

        news_obj.add_params(params)
        self.news = news_obj

        results = news_obj.make_request()
        if results.get("status", None) == "ok":
            i = results["totalResults"]
            status_text = f"Retrieved {i} results."
            
            articles = [a for a in results["articles"] if a["source"]["name"] != "[Removed]"]
            if len(articles) < i:
                j = i - len(articles)
                status_text += f" {j} articles have been removed by API source."

            self.root.statusbar.set(text=status_text)
            self.root.downloaded_results = articles 
            self.right_frame.page = 0
        
            # Show new results
            self.right_frame.show_results()
            self.right_frame.button_analytics["state"] = "normal"
            if len(self.root.downloaded_results) > self.root.page_len:
                self.right_frame.button_next["state"] = "normal"

        else: 
            status_text = results.get("message", "Error")
        # TO-DO: clean up error message
            self.root.statusbar.set(text=status_text)

    def search_news(self):
        self.root.statusbar.set(text="Downloading from NewsAPI ...")

        # Clear existing data
        self.reset_content()

        # Create news object
        if self.left_frame.news_type == 2:
            news_obj = TopHeadlines()
        else:
            news_obj = News()
        
        # Add params
        params = {}

        # Check if params are entered
        query_content = self.left_frame.query_entry.get()
        if query_content:
            params["q"] = self.left_frame.query_entry.get()
        
        language = self.left_frame.language_menu.option_var.get()
        if language:
            params["language"] = language
            print(params)
        
        country = self.left_frame.country_menu.option_var.get()
        if country:
            params["country"] = country
            print(params)

        if len(params) > 0:
            news_obj.add_params(params)
            self.news = news_obj

            results = news_obj.make_request()
            if results.get("status", None) == "ok":
                i = results["totalResults"]
                status_text = f"Retrieved {i} results."
                
                articles = [a for a in results["articles"] if a["source"]["name"] != "[Removed]"]
                if len(articles) < i:
                    j = i - len(articles)
                    status_text += f" {j} articles have been removed by API source."

                self.root.statusbar.set(text=status_text)
                self.root.downloaded_results = articles 
                self.right_frame.page = 0
            
                # Show new results
                self.right_frame.show_results()
                self.right_frame.button_analytics["state"] = "normal"
                if len(self.root.downloaded_results) > self.root.page_len:
                    self.right_frame.button_next["state"] = "normal"

            else: 
                status_text = results.get("message", "Error")
            # TO-DO: clean up error message
                self.root.statusbar.set(text=status_text)
        else:
            self.root.statusbar.set(text="Not enough search parameters entered. Try again.")

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

    def display_results(self):
        self.display = {}
        self.image = {}
        self.text = {}
        count = 0

        #for article in self.downloaded_results["articles"][:10]:
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
