import json
from time import sleep

from django.conf import settings
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wire_webdriver
from seleniumwire.request import Request

class Wire:
    """
        Clean seleinum-wire requests
    """
    def __init__(self, url: str, agent_string: str):
        self.url = url
        self.agent_string = agent_string

    def get_driver_option(self):
        profile_dir = str(settings.BASE_DIR / "http_requests_viewer/profile")
        option = Options()
        option.add_argument(f"--user-data-dir={profile_dir}")
        option.add_argument(f"--start-maximized")
        option.add_argument(f"user-agent={self.agent_string}")

        return option

    def get_http_requests(self, debug: bool=False,**kwargs):
        options = self.get_driver_option()
        driver = wire_webdriver.Chrome(options=options, seleniumwire_options=kwargs)
        driver.get(self.url)
        if debug:
            print("Waiting for 'continue' command")
            breakpoint()
        else:
            sleep(3)

        http_requests = self.clean_http_requests(driver.requests)
        driver.quit()
        return http_requests


    def clean_http_requests(self, http_requests: list[Request]):
        cleaned_requests = []

        for r in http_requests:
            request_dict = r.__dict__
            new_clean_current = request_dict.copy()
            new_clean_current['params'] = r.params
            new_clean_current['content_type'] = {
                "request": r.headers.get_content_type(), 
                "response": r.response.headers.get_content_type() if r.response else "",
            }
            self.clean_more(copy=new_clean_current, original=request_dict)

            if request_dict.get("response", None):
                request_response_dict = request_dict['response'].__dict__
                new_clean_current['response'] = request_response_dict.copy()

                self.clean_more(copy=new_clean_current['response'], original=request_response_dict)

            del new_clean_current['ws_messages']
            del new_clean_current['cert']

            cleaned_requests.append(new_clean_current)

        return cleaned_requests

    def clean_more(self, copy, original):
        """
            Clean body, date, headers
        """

        # for call in template
        try:
            copy['body'] = original['_body'].decode()
        except:
            copy['body'] = str(original['_body'])
        del copy['_body']

        copy['date'] = original['date'].strftime("%Y-%m-%d %H:%M:%S")
        copy['headers'] = original['headers'].items()