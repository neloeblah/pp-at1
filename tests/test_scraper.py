import unittest
import json
import requests

from unittest.mock import patch, Mock
from bs4 import BeautifulSoup

from scraper import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.scraper = Scraper(self.url)
        
    @patch('scraper.requests.get')
    def test_make_request_success(self, mock_get):
        mock_response = Mock()
        mock_response.content = "<html></html>"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        self.scraper.make_request()
        
        self.assertIsNotNone(self.scraper.html)
        self.assertEqual(self.scraper.page.title, None)
        self.assertIsNone(self.scraper.error)
    
    @patch('scraper.requests.get')
    def test_make_request_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Error making request")
        
        self.scraper.make_request()
        
        self.assertIsNone(self.scraper.html)
        self.assertIsNotNone(self.scraper.error)
        
    def test_check_status(self):
        self.scraper.html = Mock()
        self.scraper.html.status_code = 200
        
        self.assertEqual(self.scraper.check_status(), 200)
        
        self.scraper.html = None
        self.assertEqual(self.scraper.check_status(), -1)
    
    def test_count_adverts(self):
        html_content = """
            <div class="_ad">Ad 1</div>
            <div class="content">Main Article Here</div>
            <div class="advert">Ad 2</div>
        """

        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        self.scraper.html = Mock()
        self.scraper.html.status_code = 200
        
        self.scraper.count_adverts()

        self.assertEqual(self.scraper.ad_count, 2)
    
    def test_count_scripts(self):
        html_content = """
            <script>hidead<div>Blah blah blah</div></script>
            <script>Mores scripts </script>
        """

        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        self.scraper.html = Mock()
        self.scraper.html.status_code = 200
        
        self.scraper.count_scripts()

        self.assertEqual(self.scraper.script_count, 1)
        
    def test_extract_content(self):
        html_content = "<meta property='og:title' content='Test Title'>"
        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        
        content = self.scraper.extract_content(prop="og:title")

        self.assertEqual(content, "Test Title")
        
    def test_get_linked_data(self):
        linked_data = {
            "@context": "https://example.com",
            "@type": "News",
            "author": {"@type": "Person", "name": "Lebron James"},
            "articleSection": "Technology",
            "keywords": "Tech, News"
        }

        json_data = json.dumps(linked_data)
        html_content = f"<script type='application/ld+json'>{json_data}</script>"
        
        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        self.scraper.get_linked_data()
        
        self.assertEqual(self.scraper.author, {"@type": "Person", "name": "Lebron James"})
        self.assertEqual(self.scraper.section, "Technology")
        self.assertEqual(self.scraper.keywords, "Tech, News")
    
    def test_get_facebook(self):
        html_content = "<meta property='fb:page_id' content='12345'>"
        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        
        self.scraper.get_facebook()

        self.assertIn("facebook.com/12345", self.scraper.socials)
        
    def test_get_twitter(self):
        html_content = """
            <meta name="twitter:site" content="@example">
            <meta name="twitter:creator" content="@creator">
        """

        self.scraper.page = BeautifulSoup(html_content, "html.parser")
        
        self.scraper.get_twitter()

        self.assertIn("x.com/@example", self.scraper.socials)
        self.assertIn("x.com/@creator", self.scraper.socials)

    def test_str_method(self):
        self.scraper.url = "https://example.com"
        self.scraper.ad_count = 5
        self.scraper.script_count = 2
        self.scraper.socials = ["facebook.com/test", "x.com/test"]
        self.scraper.author = {"@type": "Person", "name": "Jebron Lames"}
        self.scraper.section = "Technology"
        self.scraper.keywords = "Tech, News"
        
        expected_output = (
            "URL: https://example.com\n"
            "Ads: 7\n"
            "Socials: facebook.com/test, x.com/test\n"
            "Author details: {'@type': 'Person', 'name': 'Jebron Lames'}\n"
            "News Section: Technology\n"
            "Keywords: Tech, News\n"
        )
        self.assertEqual(str(self.scraper), expected_output)

if __name__ == '__main__':
    unittest.main()