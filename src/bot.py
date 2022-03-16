import time

from colored import fg
from pynput.keyboard import Controller, Key
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())
keyboard = Controller()


class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        pass

    def run(self):
        pass
