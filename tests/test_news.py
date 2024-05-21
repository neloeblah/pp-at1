import unittest
from unittest.mock import patch
from newsapi import News, TopHeadlines, Sources

class TestNewsAPI(unittest.TestCase):

    def setUp(self):
        self.news = News()

    def test_set_params_invalid(self):
        params = {'invalid_param': 'value'}
        self.news.add_params(params)
        
        self.assertNotIn('invalid_param', self.news._News__params)

    def test_set_params_valid(self):
        params = {'q': 'Test', 'language': 'en'}
        self.news.add_params(params)

        self.assertEqual(self.news._News__params['q'], 'Test')
        self.assertEqual(self.news._News__params['language'], 'en')

    def test_set_params_exclusive(self):
        top_headlines = TopHeadlines()
        params = {'sources': 'bbc-news', 'country': 'us'}
        top_headlines.add_params(params)

        self.assertIn('sources', top_headlines._News__params)
        self.assertNotIn('country', top_headlines._News__params)

    def test_check_params_entries(self):
        params = {'q': 'Python' * 100, 'language': 'xx', 'from': 'invalid-date', 'pageSize': 200}
        self.news.add_params(params)
        self.news.check_param_entries()

        self.assertEqual(len(self.news._News__params['q']), 500)
        self.assertNotIn('language', self.news._News__params)
        self.assertNotIn('from', self.news._News__params)
        self.assertEqual(self.news._News__params['pageSize'], 100)

    @patch('newsapi.requests.get')
    def test_make_request(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'ok',
            'articles': [{'title': 'Test News'}]
        }

        result = self.news.make_request()

        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['articles'][0]['title'], 'Test News')

    @patch('newsapi.requests.get')
    def test_make_request_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'error',
            'code': 'apiKeyInvalid',
            'message': 'Your API key is invalid.'
        }

        result = self.news.make_request()

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['code'], 'apiKeyInvalid')
        self.assertEqual(result['message'], 'Your API key is invalid.')

if __name__ == '__main__':
    unittest.main()