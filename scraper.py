import json
import requests
import re

from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.page = None
        self.ad_count = None
        self.script_count = None
        self.socials = []
        self.author = None
        self.section = None
        self.keywords = None

    def make_request(self):
        if self.url != "https://removed.com":
            self.html = requests.get(self.url)
            self.page = BeautifulSoup(self.html.content, "html.parser")
    
    def count_adverts(self):
        if self.html.status_code == 403:
            self.ad_count = -1
        elif self.html.status_code == 200:
            pattern = re.compile(r"_ad|-ad|advert|adwrap|^ad-|^ad_", re.IGNORECASE)
            ads = self.page.find_all('div', class_=lambda c: c and pattern.search(c))

            self.ad_count = len(ads)
        
    def count_scripts(self, script_type="hidead"):
        if self.html.status_code == 403:
            self.script_count = -1
        elif self.html.status_code == 200:
            scripts = self.page.find_all('script')

            self.script_count = 0
            for s in scripts:
                s_text = s.get_text().lower()
                if s_text.count(script_type) > 0 and s_text.count("div") > 0:
                    self.script_count += 1

    def extract_content(self, prop=None, attrs=None):
        if prop:
            tag = self.page.find('meta', property=prop)
        elif attrs:
            tag = self.page.find('meta', attrs=attrs)
        
        if tag:
            return tag.get("content", None)
        else:
            return None

    def get_linked_data(self):
        ld = self.page.find("script", type="application/ld+json")

        if ld:
            extract = json.loads(ld.string)
            
            if type(extract) == list: 
                extract = extract[0]

            self.author = extract.get("author", None)  # dictionary keys: @type, name, sameAs, url, description
            self.section = extract.get("articleSection", None)
            self.keywords = extract.get("keywords", None)

    def get_facebook(self):
        # Check page id as primary source
        fb_id = self.extract_content(prop="fb:page_id")
        
        # Use pages if only one entry and page id is missing
        if not fb_id:
            fb_pages = self.extract_content(prop="fb:pages")
        
            if fb_pages.count(",") == 0:
                fb_id = fb_pages
        
        # Add to socials if available
        if fb_id:
            self.socials.append(f"facebook.com/{fb_id}")

    def get_twitter(self):
        # Twitter links can be for author, publisher or both
        site = self.extract_content(attrs={"name": "twitter:site"})
        creator = self.extract_content(attrs={'name': 'twitter:creator'})

        # Add to socials if available
        if site:
            self.socials.append(f"x.com/{site}")
        
        if creator:
            self.socials.append(f"x.com/{creator}")

    def get_mastodon(self):
        mastodon_pattern = re.compile(r'.*mastodon\.social/@.*', re.IGNORECASE)
        mastodon = self.page.find('link', href=mastodon_pattern)

        if mastodon:
            at = mastodon.get("content", None)
            self.socials.append(at)

    def get_socials(self):
        self.get_facebook()
        self.get_twitter()
        self.get_mastodon()

    def __str__(self):
        text = "URL: " + self.url + "\n"
        ads = self.ad_count + self.script_count
        text += "Ads: " + str(ads) + "\n"
        text += "Socials: " + ", ".join(self.socials) + "\n"
        text += "Author details: " + str(self.author) + "\n"
        text += "News Section: " + str(self.section) + "\n"
        text += "Keywords: " + str(self.keywords) + "\n"
        
        return text
