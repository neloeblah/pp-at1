import requests

class News():
    __api_key = "pub_42895a6190c2c322f71e0711a56626acb3433"
    # base_url = "https://newsdata.io/api/1/news?apikey="
    base_url = "https://newsdata.io/api/1/news"
    credit = 200 # per day
    rate_limit = 30 # per 15 min
    
    # Only api key required, rest are optional
    valid_params = {
        "apiKey", 
        "id", # up to 50 comma separated (e.g. article_id_1,article_id_2,...)
        "q", "qInTitle", "qInMeta", # Mutually exclusive, url-encoded, 512 character limit
        "timeframe", # Hours or minutes. 1-48 for hours, 1m to 2880m for minutes
        "country", # Up to 5 comma-separated. 
        "category", "excludecategory", # Mutually exclusive. Up to 5 comma-separated. 
        "language", "domain", "domainurl", "excludedomain", # Up to 5 comma-separated. 
        "prioritydomain", # top, medium or low
        "timezone", # See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        "full_content", "image", "video" # 0 or 1,
        "size", # 1 to 25 for free users
        "page"
    }

    def __init__(self, new_key=None):
        if new_key:
            News.__api_key = new_key
        
        self.__params = {
            "apiKey": News.__api_key
        }
        
    def add_params(self, params_dict):
        # TO-DO: add validation checks
        for k, v in params_dict.items():
            self.__params[k] = v

    def make_request(self):
        url = News.base_url
        response = requests.get(url, params=self.__params)
        result = response.json()

        return result
