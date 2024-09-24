import scrapy
from scrapy_splash import SplashRequest

class GlassdoorsSpider(scrapy.Spider):
    name = 'glassdoors'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'RETRY_TIMES': 3,  
        'SPLASH_URL': 'http://localhost:8050',  
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    }

    def start_requests(self):
        urls = [
            'https://www.glassdoor.com/Job/remote-us-data-scientist-jobs-SRCH_IL.0,9_IS11047_KO10,24.htm?sortBy=date_desc',
        ]
        for url in urls: 
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        # Parse the initial job listings
        jobs_selector = response.css('.JobCard_jobTitle___7I6y')
        for job in jobs_selector:
            job_link = job.css('::attr(href)').get()
            if job_link:
                job_url = response.urljoin(job_link)
                print(f"Job URL: {job_url}")
                yield {'Job URL': job_url}

        # Scroll down to load more job listings
        yield SplashRequest(
            url=response.url,
            callback=self.parse_scroll,
            endpoint='execute',
            args={'lua_source': self.scroll_script},
            dont_filter=True
        )

    def parse_scroll(self, response):
        jobs_selector = response.css('.JobCard_jobTitle___7I6y')
        for job in jobs_selector:
            job_link = job.css('::attr(href)').get()
            if job_link:
                job_url = response.urljoin(job_link)
                print(f"Job URL: {job_url}")
                yield {'Job URL': job_url}

    @property
    def scroll_script(self):
        # Lua script
        return """
        function main(splash)
            local scroll_delay = 1  -- Delay between each scroll in seconds
            local scroll_count = 6  -- Number of times to scroll
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc("function() { return document.body.scrollHeight; }")

            splash:set_viewport_size(1920, 1080)
            splash:go(splash.args.url)
            splash:wait(2)

            for _ = 1, scroll_count do
                local prev_height = get_body_height()
                scroll_to(0, prev_height)
                splash:wait(scroll_delay)
            end

            return splash:html()
        end
        """
