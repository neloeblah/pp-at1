import tkinter as tk
import plotly.express as px
import os
import pandas as pd
from PIL import ImageTk, Image

names_dict = {'Business Insider': 4,
 'NPR': 5,
 'ESPN': 27,
 'Ars Technica': 1,
 'The Athletic': 1,
 'CNET': 1,
 'ABC News': 1,
 'ReadWrite': 3,
 'MacRumors': 2,
 'Buzzfeed': 1,
 'Le Monde': 12,
 'Digital Trends': 7,
 'Android Police': 1,
 '9to5Mac': 1,
 'HYPEBEAST': 4,
 'Rolling Stone': 1,
 'Yahoo Entertainment': 1,
 'Bleacher Report': 8,
 'Hipertextual': 1,
 'GameSpot': 1,
 'Die Zeit': 12,
 'Slashdot.org': 1,
 'BBC News': 1,
 'Presse-citron': 1}
df = pd.DataFrame.from_dict(names_dict, orient="index").reset_index()
df.columns = ["Source", "Count"]
df.sort_values("Count", inplace=True)

n = len(df)
if n > 10:
    top_10 = df.tail(10)
    rest = df.head(n-10).copy()
    rest["Source"] = "Other"
    rest = rest.groupby("Source", as_index=False)["Count"].sum()
    
    CHART_DF = pd.concat([rest, top_10]).reset_index(drop=True)
else:
    CHART_DF = df


cols = ["name",	"count",	"mean"]
data = [
["9to5Mac",	1,	2519.000000],
["ABC News",	1,	2009.000000],
["Android Police",	1,	6570.000000],
["Ars Technica",	1,	5447.000000],
["Bleacher Report",	7,	1770.571429],
["Business Insider",	4,	3538.250000],
["Buzzfeed",	1,	279.000000],
["CNET",	1,	2155.000000],
["Die Zeit",	12,	2868.000000],
["Digital Trends",	7,	2943.571429]
]
OTHER_DF = pd.DataFrame(data, columns=cols)

class ContentFrame(tk.Frame):
    def __init__(self, root, bg_color, text_color):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.cached = {}
        self.page = 0
        self.page_len = 5
        self.analytics_content = None
        self.show_content = True
        tk.Frame.__init__(self, root, width=800, highlightbackground="black", highlightthickness=1, bg=bg_color)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


class GraphFrame():
    def __init__(self, root, bg_color, text_color):
        self.root = root
        self.bg_color = bg_color
        self.text_color = text_color
        self.plots = {}
        self.labels = {}

        # Create subfolder if required
        if not os.path.exists("images"):
            os.mkdir("images")
        else:
            # Clear existing files 
            for f in os.listdir("images"):
                os.remove(f"images/{f}")
        
        # Create plots and save pngs
        self.create_count_plot()
        self.create_len_plot()

        # Display plots
        filenames = ["fig_source_count.png", "fig_source_length.png", "fig_source_count.png", "fig_source_length.png"]
        for i, filename in enumerate(filenames):
            self.display_bar_plot(filename, counter=i)

    def create_count_plot(self):
        self.source_df = CHART_DF

        colors = ["#A5A4AC", "#018ADA"]
        self.source_df["Color"] = colors[0]
        self.source_df.loc[self.source_df["Source"] == "Other", "Color"] = colors[1]

        fig = px.bar(self.source_df, x="Count", y="Source", color="Color", orientation="h", 
                     color_discrete_sequence=colors,
                     width=400, height=300, template="plotly_dark")
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        fig.write_image("images/fig_source_count.png")

    def create_len_plot(self):
        self.length_df = OTHER_DF

        colors = ["#A5A4AC", "#018ADA"]
        self.length_df["Color"] = colors[0]
        self.length_df.loc[self.length_df["name"] == "9to5Mac", "Color"] = colors[1]

        fig = px.bar(
            self.length_df, x='mean', y='name', color="Color", orientation='h', 
            color_discrete_sequence=colors,
            width=400, height=300,
            labels={'name': 'Source', 'mean': 'Length (avg.)'}, 
            template='plotly_dark'
        )
        fig.add_vline(x=self.length_df["mean"].mean(), line_color="#9D0620", line_dash="dot")
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        fig.write_image("images/fig_source_length.png")

    def display_bar_plot(self, filename, counter):
        if os.path.isfile(f"images/{filename}"):
            # Load image
            img = Image.open(f"images/{filename}")
            self.plots[counter] = ImageTk.PhotoImage(img)

            # GUI img label
            row = counter // 2
            col = counter % 2
            self.labels[counter] = tk.Label(self.root, image=self.plots[counter], bg=self.bg_color)
            self.labels[counter].grid(row=row, column=col, sticky='nsew')
            self.labels[counter].image = self.plots[counter]

class MainApp():
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("News Aggregator")

        self.chart_frame = ContentFrame(root, bg_color="#FFF1C8", text_color="#000000")
        self.chart_frame.pack_propagate(False)

        self.graph_frame = tk.Frame()
        self.chart_test = GraphFrame(self.graph_frame, bg_color="#FFF1C8", text_color="#000000")
        self.graph_frame.pack(in_=self.chart_frame)


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
