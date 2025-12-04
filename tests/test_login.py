import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Creating a test class
class TestLogin(unittest.TestCase):

    # Initialising a webdriver
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login(self):
        driver = self.driver
        driver.get("https://127.0.0.1:5000/")