# News Aggregator Project

## Overview

This News Aggregator project is a Python-based application built with Tkinter for the GUI. It fetches news headlines from a news aggregator API, scrapes these websites using BeautifulSoup for additional information such as writer social media contacts and the number of ads on the page, and displays analytics via graphs.

## Features

- **Fetch News Headlines:** Retrieves news headlines from a news aggregator API.
- **Web Scraping:** Uses BeautifulSoup to scrape news websites for additional information including writer social media contacts and the number of ads.
- **Analytics:** Displays graphs showing the top news sources, article lengths per source, and a timeline of when articles are published.
- **Graphical User Interface:** Built with Tkinter, providing a user-friendly interface.

## Installation

### Prerequisites

- Python 3.x
- Poetry (for dependency management)

## Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/neloeblah/pp-at1.git
   cd pp-at1
   ```

2. **Install dependencies:**
   ```sh
   poetry install
   ```

3. **Run the application:**
   ```sh
   poetry run python app.py
   ```

### Usage

1. **Search News:**
    - Enter a search query in the search box.
    - Optionally select a country and language from the dropdown menus.
    - Click the "Search" button to fetch news headlines.

2. **Navigate Results:**
    - Use the "Next" and "Last" buttons to cycle through the news articles.
    - Toggle between article content and analytics using the "Analytics" button.

3. **View Analytics:**
    - The application displays graphs showing the top news sources, article lengths per source, and a timeline of article publication.

## Tests

### Running Tests
The project includes tests for the GUI, news API, and scraping functionalities. The `tests` are located in the tests directory.

To run the tests, use the following command:

```sh
poetry run python -m unittest discover -s tests
```

Project Structure
```graphql
pp-at1/
│
├── app.py                    # Main application file
├── newsapi.py                # News API interaction code
├── scraper.py                # Web scraping code
├── graph.py                  # Data visualisation code
├── README.md                 # Project documentation
├── pyproject.txt             # Project dependencies
├── __init__.py               # Initialize the package
├── tests/                    # Test suite
│   ├── test_news.py          # Tests for news API interactions
│   ├── test_scraper.py       # Tests for web scraping
│   └── test_gui.py           # Tests for the Tkinter GUI
├── images/                   # Cache for plotly express graphs
│   ├── ... 
└── ...
```

## References 
- [News API](https://newsapi.org/)  provides the news headlines. Endpoints were accessed directly through `requests`, no additional packages were used.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) was used for web scraping capabilities.
- [Plotly Express](https://plotly.com/python/plotly-express/) was used graphing and analytics.
