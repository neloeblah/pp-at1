import datetime
import requests

class News():
    __api_key = "3b8c7e9d0e2c43a7bc2083b63ec7b313"
    base_url = "https://newsapi.org"
    valid_params = {"apiKey", "q", "searchIn", "sources", "domains", "excludeDomains", "from", "to", "language", "sortBy", "pageSize", "page"}

    def __init__(self, api_key=None):
        if api_key:
            News.__api_key = api_key

        # Encapsulate params to hide API Key
        self.__params = {
            "apiKey": News.__api_key
        }
        self.end_point = "/v2/everything"
        self.removed_params = []
        self.errors = None
        self.warnings = []

    def __remove_invalid_parameters(self, new_params, valid_params):
        # Remove parameters not accepted by API
        removed_params = new_params - valid_params
        
        # for p in removed_params:
        #     print(f"Removed invalid parameter '{p}'.")

        self.removed_params += removed_params

        return new_params & valid_params
    
    def __remove_exclusive_parameters(self, new_params_set, exclusive_params):
        # Remove parameters that can't be used together
        if len(new_params_set & exclusive_params) > 1:
            removed_country = new_params_set.discard("country")
            if removed_country != None:
                self.removed_params.append('country')
                # print("Removed 'country' due to conflicting parameters.")

            if len(new_params_set & exclusive_params) > 1:
                removed_category = new_params_set.discard("category")
                if removed_category != None:
                    self.removed_params.append('category')
                    # print("Removed 'category' due to conflicting parameters.")
        
        return new_params_set

    def set_params(self, new_params_dict, valid_params, exclusive_params=None):
        # Create set for checking
        new_params_set = set(new_params_dict.keys())
        
        # Remove invalid parameters
        new_params_set = self.__remove_invalid_parameters(new_params_set, valid_params)

        # Remove parameters that can't be used together
        if exclusive_params is not None:
            new_params_set = self.__remove_exclusive_parameters(new_params_set, exclusive_params)

        # Add successful parameters
        if len(new_params_set) > 0:
            for p in new_params_set:
                self.__params[p] = new_params_dict[p]
        else:
            self.errors = "No valid parameters available to add"

    def check_param_entries(self):
        # Query limit
        if len(self.__params.get("q", "")) > 500:
            self.__params["q"] = self.__params["q"][:500]
            self.warnings.append("'q' limited to 500 characters. ")
            # print("q length too long, limited to first 500 characters.")

        # Sources  limit
        def __limit_sources(sources, cutoff=19):
            # Recursive loop to reduce sources over the limit
            if sources.count(",") == cutoff:
                return sources
            return __limit_sources(sources[:sources.rfind(",")])

        if self.__params.get("sources", "").count(",") > 19:
            self.__params["sources"] = __limit_sources(self.__params["sources"])
            self.warnings.append("'sources' limited to 20.")
            # print("Too many sources, reduced to 20.")

        # Check dates
        def __test_date(date_str):
            try:
                datetime.datetime.fromisoformat(date_str)
            except:
                return False
            return True
        
        for d in ["from", "to"]:
            date_str = self.__params.get(d, None)
            date_flag = __test_date(date_str)

            if not date_flag and date_str != None:
                del self.__params[d]
                self.warnings.append("Invalid 'd' removed. ")
                # print(f"Invalid date format entered for '{d}', parameter removed.")

        # Language options
        languages = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh']
        lang_str = self.__params.get("language", None)
        if lang_str not in languages and lang_str != None:
            del self.__params["language"]
            self.warnings.append("Invalid 'language' removed. ")
            # print("Invalid language entered, parameter removed.")

        # Country options
        countries = [
            'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
            'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
            'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
            'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'
        ]
        country_str = self.__params.get("country", None)
        if country_str not in countries and country_str != None:
            del self.__params["country"]
            self.warnings.append("Invalid 'country' removed. ")
            # print("Invalid country entered, parameter removed.")

        # Category options
        categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        category_str = self.__params.get("category", None)
        if category_str not in categories and category_str != None:
            del self.__params["category"]
            self.warnings.append("Invalid 'category' removed. ")
            # print("Invalid category entered, parameter removed.")

        # sortBy options
        sort_by = ["relevancy", "popularity", "publishedAt"]
        sort_str = self.__params.get("sortBy", None)
        if sort_str not in sort_by and sort_str != None:
            self.__params["sortBy"] = "publishedAt"
            self.warnings.append("Invalid 'publishedAt' removed. ")
            # print("sortBy invalid, set to default 'publishedAt'.")

        # pageSize limit
        page_size = self.__params.get("pageSize", 100)
        if page_size > 100 or page_size < 0 or type(page_size) == str:
            self.__params["pageSize"] = 100
            self.warnings.append("Invalid 'pageSize' removed. ")
            # print("pageSize invalid, set to default 100.")

        # Check page number
        try:
            if self.__params.get("page", None) != None: int(self.__params["page"])
        except:
            self.__params["page"] = 1
            self.warnings.append("Invalid 'page', reset to 1. ")
            # print("page invalid, set to default 1.")

    def add_params(self, new_params_dict):
        # Pass params to setter with validation checks
        self.set_params(new_params_dict, News.valid_params)

    def show_available_params(self):
        param_str = ", ".join(News.valid_params)
        print(f"Available parameters for NewsAPI Everything endpoint are '{param_str}'")
        
    def make_request(self):
        # API request
        url = News.base_url + self.end_point
        response = requests.get(url, params=self.__params)
        result = response.json()

        # Check status
        # if result["status"] == "error":
        #     print("Error:")
        #     print(result["code"])
        #     print(result["message"])
        #     return None
        # else:
        #     return result
        
        return result


class TopHeadlines(News):
    valid_params = {"apiKey", "sources", "category", "country", "q", "pageSize", "page"}
    exclusive_params = {"sources", "category", "country"}

    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.end_point = "/v2/top-headlines"

    def add_params(self, new_params_dict):
        # Pass params to setter with validation checks
        self.set_params(new_params_dict, TopHeadlines.valid_params, TopHeadlines.exclusive_params)

    def show_available_params(self):
        param_str = ", ".join(TopHeadlines.valid_params)
        print(f"Available parameters for NewsAPI TopHeadlines endpoint are '{param_str}'")


class Sources(News):
    valid_params = {"apiKey", "q", "searchIn", "sources", "excludeDomains", "from", "to", "language", "sortBy", "pageSize", "page"}

    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.end_point = '/v2/top-headlines/sources'

    def add_params(self, new_params_dict):
        # Pass params to setter with validation checks
        self.set_params(new_params_dict, Sources.valid_params)

    def show_available_params(self):
        param_str = ", ".join(Sources.valid_params)
        print(f"Available parameters for NewsAPI Sources endpoint are '{param_str}'")
