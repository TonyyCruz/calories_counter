from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class AuthorBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, time=5):
        sleep(time)

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def get_form(self, xpath=None, class_name=None):
        if xpath is not None:
            return self.browser.find_element(
                By.XPATH,
                f"{xpath}"
            )
        if class_name is not None:
            return self.browser.find_element(
                By.CLASS_NAME,
                f"{class_name}"
            )
