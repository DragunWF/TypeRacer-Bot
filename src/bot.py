import time
import random
from pynput.keyboard import Controller, Key
from utils import Utilities

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
keyboard = Controller()


class Bot:
    def __init__(self, username, password, session, races, universe):
        self.username = username
        self.password = password
        self.session = session

        self.races_to_play = races
        self.finished_races = 0
        self.key_intervals = (0.085, 0.090, 0.095)

        self.url = "https://play.typeracer.com/"
        if universe != "play":
            self.url += f"?universe={universe}"

        driver.get(self.url)

    def login(self):
        sign_in = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        time.sleep(0.1)

        username = driver.find_element_by_name("username")
        username.send_keys(self.username)
        password = driver.find_element_by_name("password")
        password.send_keys(self.password)
        time.sleep(0.05)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(2)

        driver.get(self.url)
        time.sleep(0.1)

    def enter_race(self):
        start_game = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Enter a Typing Race"))
        )
        start_game.click()
        time.sleep(0.05)

    def new_race(self):
        new_race = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Race again"))
        )
        new_race.click()
        time.sleep(0.1)

    def race(self):
        input_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inputPanel"))
        )
        race_text = input_panel.text.split("\n")[0]

        while True:
            game_time = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "lightLabel"))
            )
            if game_time.text == "Go!":
                break
            time.sleep(0.2)

        for character in race_text:
            keyboard.type(character)
            time.sleep(random.choice(self.key_intervals))

        self.session.race_counts += 1
        time.sleep(0.1)

    def exit(self):
        Utilities.tts_print("Shutting down in...", color="yellow")

        number_words = ("one", "two", "three")
        for i in range(3):
            time_to_quit = 4 - (i + 1)
            color = "yellow" if time_to_quit > 2 else "red"
            Utilities.colored_print(f"{time_to_quit}{'.' * time_to_quit}",
                                    color=color)
            Utilities.text_to_speech(number_words[time_to_quit - 1])

        driver.quit()

    def validate_link(self):
        content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "themeContent"))
        )
        header = content.text.split("\n")[0]

        if header == "This URL was not recognized":
            Utilities.tts_print("Make sure to put a valid universe URL next time.",
                                color="yellow")
            raise Exception("Invalid universe input")

    def run(self):
        try:
            self.validate_link()
            self.login()
            self.enter_race()

            for i in range(self.races_to_play):
                Utilities.colored_print(f"Session Race Count: {i + 1}",
                                        color="green")
                self.race()
                self.new_race()

            self.session.result = True
        except:
            self.session.result = False

        self.session.save_session()
        self.exit()
