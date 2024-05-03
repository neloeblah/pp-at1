import tkinter as tk
import datetime
import re

from tkinter import ttk
from newsapi import News, TopHeadlines
from PIL import ImageTk, Image
import io
import requests
import webbrowser


articles = [
            {'source': {'id': None, 'name': '[Removed]'}, 'author': None, 'title': '[Removed]', 'description': '[Removed]', 'url': 'https://removed.com', 'urlToImage': None, 'publishedAt': '1970-01-01T00:00:00Z', 'content': '[Removed]'}, 
            {'source': {'id': 'bbc-sport', 'name': 'BBC Sport'}, 'author': None, 'title': 'NBA play-offs: Tyrese Haliburton leads Indiana Pacers to win over Milwaukee Bucks', 'description': 'Tyrese Haliburton converts a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series.', 'url': 'http://www.bbc.co.uk/sport/basketball/articles/cg30zl29mzlo', 'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_sport/7f48/live/1c411940-045e-11ef-b9d8-4f52aebe147d.jpg', 'publishedAt': '2024-04-27T07:52:13.3513784Z', 'content': 'Tyrese Haliburton converted a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series… [+864 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Cleveland Cavaliers vs. Orlando Magic NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Find out how and when to watch Game 4 of the Cavaliers vs. Magic NBA Playoffs series, even if you don't have cable.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-cavaliers-vs-magic-nba-playoffs-game-game-4-livestream-options-start-time-and-more/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/6570261c-23f8-4c32-8417-2cfd5148e080/thumbnail/1200x630/98546cb5680e0d153001f7a7148851d3/gettyimages-2150246951-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T05:06:47+00:00', 'content': 'Darius Garland #10 of the Cleveland Cavaliers dribbles the ball against Paolo Banchero #5 of the Orlando Magic during the third quarter of game three of the Eastern Conference First Round Playoffs at… [+8406 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Here's how and when to watch Game 4 of the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-denver-nuggets-vs-los-angeles-lakers-game-4/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/0d01dd18-1c25-4fcb-9c8d-1b080342a800/thumbnail/1200x630/3d5ceb8e0d7954dbedd2664d016fbfbf/gettyimages-2150339085-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:59:00+00:00', 'content': 'Nikola Jokic #15 of the Denver Nuggets during game three of the Western Conference First Round Playoffs at Crypto.com Arena on April 25, 2024 in Los Angeles, California.\r\nRonald Martinez/Getty Images… [+10776 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Boston Celtics vs. Miami Heat NBA Playoffs game tonight: Game 3 livestream options, start time, more', 'description': "Game 3 of the Celtics vs. Heat NBA Playoffs series is can't-miss basketball. Here's how and when to watch tonight.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-boston-celtics-vs-miami-heat-nba-playoffs-game-3/', 'urlToImage': 'https://assets1.cbsnewsstatic.com/hub/i/r/2024/04/26/09ef6820-2df5-4120-96f9-5d8884a6543e/thumbnail/1200x630/6d15d84003a1d8c8726ff8e1dfb5501b/gettyimages-2149460985-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:47:00+00:00', 'content': 'Tyler Herro #14 of the Miami Heat looks at his bench after making a three-point basket against the Boston Celtics during the second quarter of game two of the Eastern Conference First Round Playoffs … [+8404 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the OKC Thunder vs. New Orleans Pelicans NBA Playoffs game tonight: Game 3 livestream options, more', 'description': "Here's how and when to watch Game 3 of the OKC Thunder vs. New Orleans Pelicans NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-okc-thunder-vs-new-orleans-pelicans-nba-playoffs-game-3/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/85e98138-3298-4ec7-a1a7-e5030b12aa2d/thumbnail/1200x630/a5861ab2092c404f418cfb7687dd2d1c/gettyimages-2150073262-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:10:19+00:00', 'content': 'Oklahoma City Thunder players react from the bench after a three-pointer during game two of the first round of the NBA playoffs against the New Orleans Pelicans at Paycom Center on April 24, 2024 in … [+8574 chars]'}, 
            {'source': {'id': 'abc-news-au', 'name': 'ABC News (AU)'}, 'author': 'ABC News', 'title': "Joel Embiid fights Bell's palsy to drop NBA playoff career high as Sixers down Knicks", 'description': 'Philadelphia 76ers star Joel Embiid went to the doctors complaining of a migraine prior to the playoffs, only for the diagnosis to be something more sinister that impacts how he looks on the court.', 'url': 'https://www.abc.net.au/news/2024-04-26/nba-playoffs-joel-embiid-bells-palsy-sixers-knicks-game-3/103773714', 'urlToImage': 'https://live-production.wcms.abc-cdn.net.au/d8406c6fa93bfc53f1dd55f9976d5d2a?impolicy=wcms_watermark_news&cropH=2531&cropW=4500&xPos=0&yPos=338&width=862&height=485&imformat=generic', 'publishedAt': '2024-04-26T05:28:24Z', 'content': "<ul><li>In short:\xa0Joel Embiid has been diagnosed with Bell's palsy, a form of facial paralysis, after initially complaining of migraines prior to the NBA playoffs.</li><li>Embiid battled through the … [+2061 chars]"},
        ]

articles2 = [
            {'source': {'id': None, 'name': '[Removed]'}, 'author': None, 'title': '[Removed]', 'description': '[Removed]', 'url': 'https://removed.com', 'urlToImage': None, 'publishedAt': '1970-01-01T00:00:00Z', 'content': '[Removed]'}, 
            {'source': {'id': 'bbc-sport', 'name': 'BBC Sport'}, 'author': None, 'title': 'NBA play-offs: Tyrese Haliburton leads Indiana Pacers to win over Milwaukee Bucks', 'description': 'Tyrese Haliburton converts a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series.', 'url': 'http://www.bbc.co.uk/sport/basketball/articles/cg30zl29mzlo', 'urlToImage': 'https://ichef.bbci.co.uk/news/1024/branded_sport/7f48/live/1c411940-045e-11ef-b9d8-4f52aebe147d.jpg', 'publishedAt': '2024-04-27T07:52:13.3513784Z', 'content': 'Tyrese Haliburton converted a three-point play with 1.6 seconds left in overtime to give the Indiana Pacers a 2-1 lead over the Milwaukee Bucks in their Eastern Conference first-round play-off series… [+864 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Cleveland Cavaliers vs. Orlando Magic NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Find out how and when to watch Game 4 of the Cavaliers vs. Magic NBA Playoffs series, even if you don't have cable.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-cavaliers-vs-magic-nba-playoffs-game-game-4-livestream-options-start-time-and-more/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/6570261c-23f8-4c32-8417-2cfd5148e080/thumbnail/1200x630/98546cb5680e0d153001f7a7148851d3/gettyimages-2150246951-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T05:06:47+00:00', 'content': 'Darius Garland #10 of the Cleveland Cavaliers dribbles the ball against Paolo Banchero #5 of the Orlando Magic during the third quarter of game three of the Eastern Conference First Round Playoffs at… [+8406 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs game tonight: Game 4 livestream options, more', 'description': "Here's how and when to watch Game 4 of the Denver Nuggets vs. Los Angeles Lakers NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-denver-nuggets-vs-los-angeles-lakers-game-4/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/0d01dd18-1c25-4fcb-9c8d-1b080342a800/thumbnail/1200x630/3d5ceb8e0d7954dbedd2664d016fbfbf/gettyimages-2150339085-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:59:00+00:00', 'content': 'Nikola Jokic #15 of the Denver Nuggets during game three of the Western Conference First Round Playoffs at Crypto.com Arena on April 25, 2024 in Los Angeles, California.\r\nRonald Martinez/Getty Images… [+10776 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the Boston Celtics vs. Miami Heat NBA Playoffs game tonight: Game 3 livestream options, start time, more', 'description': "Game 3 of the Celtics vs. Heat NBA Playoffs series is can't-miss basketball. Here's how and when to watch tonight.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-tonights-boston-celtics-vs-miami-heat-nba-playoffs-game-3/', 'urlToImage': 'https://assets1.cbsnewsstatic.com/hub/i/r/2024/04/26/09ef6820-2df5-4120-96f9-5d8884a6543e/thumbnail/1200x630/6d15d84003a1d8c8726ff8e1dfb5501b/gettyimages-2149460985-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:47:00+00:00', 'content': 'Tyler Herro #14 of the Miami Heat looks at his bench after making a three-point basket against the Boston Celtics during the second quarter of game two of the Eastern Conference First Round Playoffs … [+8404 chars]'}, 
            {'source': {'id': 'cbs-news', 'name': 'CBS News'}, 'author': 'Meredith Gordon', 'title': 'How to watch the OKC Thunder vs. New Orleans Pelicans NBA Playoffs game tonight: Game 3 livestream options, more', 'description': "Here's how and when to watch Game 3 of the OKC Thunder vs. New Orleans Pelicans NBA Playoffs series.", 'url': 'https://www.cbsnews.com/essentials/how-to-watch-todays-okc-thunder-vs-new-orleans-pelicans-nba-playoffs-game-3/', 'urlToImage': 'https://assets3.cbsnewsstatic.com/hub/i/r/2024/04/26/85e98138-3298-4ec7-a1a7-e5030b12aa2d/thumbnail/1200x630/a5861ab2092c404f418cfb7687dd2d1c/gettyimages-2150073262-1.jpg?v=63c131a0051f3823d92b0d1dffb5e0e4', 'publishedAt': '2024-04-27T04:10:19+00:00', 'content': 'Oklahoma City Thunder players react from the bench after a three-pointer during game two of the first round of the NBA playoffs against the New Orleans Pelicans at Paycom Center on April 24, 2024 in … [+8574 chars]'}, 
            {'source': {'id': 'abc-news-au', 'name': 'ABC News (AU)'}, 'author': 'ABC News', 'title': "Joel Embiid fights Bell's palsy to drop NBA playoff career high as Sixers down Knicks", 'description': 'Philadelphia 76ers star Joel Embiid went to the doctors complaining of a migraine prior to the playoffs, only for the diagnosis to be something more sinister that impacts how he looks on the court.', 'url': 'https://www.abc.net.au/news/2024-04-26/nba-playoffs-joel-embiid-bells-palsy-sixers-knicks-game-3/103773714', 'urlToImage': 'https://live-production.wcms.abc-cdn.net.au/d8406c6fa93bfc53f1dd55f9976d5d2a?impolicy=wcms_watermark_news&cropH=2531&cropW=4500&xPos=0&yPos=338&width=862&height=485&imformat=generic', 'publishedAt': '2024-04-26T05:28:24Z', 'content': "<ul><li>In short:\xa0Joel Embiid has been diagnosed with Bell's palsy, a form of facial paralysis, after initially complaining of migraines prior to the NBA playoffs.</li><li>Embiid battled through the … [+2061 chars]"},
        ]

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

class MainApp:
    __api_key = ""

    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x1000")
        self.root.title("News Aggregator")
        self.cached = {}
        self.page = 0

        ##### Frames layout
        self.nav = tk.Frame(self.root)
        self.nav.pack(side=tk.TOP)
        self.display = tk.Frame(self.root)
        self.display.pack()
        
        ##### Navigation
        # Styling
        style = ttk.Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold', 'underline'))
        
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
        self.add_article_elements(target=self.cached[self.page], articles=articles)
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
            self.add_article_elements(self.cached[self.page], articles2[::-1])
        
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


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
