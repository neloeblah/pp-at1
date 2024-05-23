import tkinter as tk
import os
import re
import pandas as pd
import plotly.express as px

from PIL import ImageTk, Image

class GraphFrame:
    def __init__(self, root, bg_color, text_color, data, width, height):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.width = width
        self.height = height
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

        # Get top 10 (if available)
        n = min(10, len(df))
        self.stats_count = df.sort_values("Count", ascending=False).head(n)

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

        # Customise titles
        if name == "fig_source_count.png":
            title = "Top Sources"
            x_title = "Articles"
        else:
            title = "Article Length"
            x_title = "Words (Avg.)"

        # Plot
        fig = px.bar(df, x=x, y=y, color=y, orientation="h", 
                    color_discrete_map=color_map, title=title,
                    width=self.width/2, height=self.height/2, template="plotly_dark")
        
        # Formatting
        # Mean should be weighted average across all before the top 10 splits
        fig.add_vline(x=mean, line_color="#9D0620", line_dash="dot")
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), 
                          xaxis_title=x_title, yaxis_title=None)
        fig.write_image(f"images/{name}")

    def create_line_plot(self):
        # Remove problematic items
        df = self.stats.copy()
        df = df.loc[df["Source"] != '[Removed]']
        df = df.loc[df["Published"].notnull()]

        # Date formatting for charts
        df["Published"] = pd.to_datetime(df['Published'], format='mixed')
        df["Date"] = df['Published'].dt.date
        df = df.groupby('Date', as_index=False)["Length"].count()
        
        # Plotting
        fig = px.line(df, x='Date', y='Length', 
                      title="Published Time", 
                      width=self.width, height=self.height/2, template='plotly_dark')
        
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20),
                          yaxis_title=None, xaxis_title=None)
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
