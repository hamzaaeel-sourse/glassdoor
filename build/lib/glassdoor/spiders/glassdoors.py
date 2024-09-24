import scrapy
from scrapy_splash import SplashRequest

class GlassdoorsSpider(scrapy.Spider):
    name = 'glassdoors'

    # User agent is used to avoid getting blocked by the website
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        urls = [
            'https://www.glassdoor.com/Job/remote-us-data-scientist-jobs-SRCH_IL.0,9_IS11047_KO10,24.htm',
        ]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')  # Specify endpoint

    def parse(self, response):
        # Log the HTTP status code
        self.logger.info('Response status code: %s', response.status)
        
        # Initialize an empty dictionary to store links
        links_dict = {}

        # Check if the status code is 200
        if response.status == 200:
            # Proceed with parsing the response
            Jobs_Selector = response.css('.JobCard_jobTitle___7I6y')
            for job in Jobs_Selector:
                link = job.css('::attr(href)').get()
                if link:
                    links_dict[link] = {
                        # You can add more information here if needed
                    }

        # Yield the links dictionary
        yield links_dict
