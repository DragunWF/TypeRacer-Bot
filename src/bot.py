import random
from time import sleep
from utils import Utilities

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Bot:
    def __init__(self, username, password, session, races, universe):
        self.username = username
        self.password = password
        self.session = session

        self.races_to_play = races
        self.finished_races = 0
        self.key_intervals = (0.040, 0.045, 0.050, 0.055, 0.060)

        self.url = "https://play.typeracer.com/"
        self.session.universe = universe

        if universe != "play":
            self.url += f"?universe={universe}"

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)

    def login(self):
        sign_in = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        sleep(0.1)

        username = self.driver.find_element_by_name("username")
        username.send_keys(self.username)
        password = self.driver.find_element_by_name("password")
        password.send_keys(self.password)
        sleep(0.05)

        sign_in_btn = self.driver.find_element_by_class_name("gwt-Button")
        sign_in_btn.click()
        sleep(1.5)

        self.driver.get(self.url)
        sleep(0.1)

    def enter_race(self):
        start_game = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Enter a Typing Race"))
        )
        start_game.click()
        sleep(0.05)

    def re_enter_race(self):
        self.driver.get(self.url)
        self.enter_race()

    def new_race(self):
        new_race = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Race again"))
        )
        new_race.click()
        sleep(0.1)

    def race(self):
        error = False

        try:
            input_panel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inputPanel"))
            )
            race_text = input_panel.text.split("\n")[0]
        except:
            error = True

        if len(race_text) < 1 or error:
            self.re_enter_race()
            return False

        while True:
            game_time = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "lightLabel"))
            )
            if game_time.text == "Go!":
                break
            sleep(0.2)

        race_input = self.driver.find_element_by_class_name("txtInput")
        for character in race_text:
            if not self.driver.find_elements_by_class_name("txtInput-error"):
                race_input.send_keys(character)
                sleep(random.choice(self.key_intervals))
            else:
                self.re_enter_race()
                return False

        self.finished_races += 1
        sleep(0.1)

        return True

    def exit(self):
        Utilities.tts_print("Shutting down in...", color="yellow")

        number_words = ("one", "two", "three")
        for i in range(3):
            seconds_to_exit = 4 - (i + 1)
            color = "yellow" if seconds_to_exit > 1 else "red"
            Utilities.colored_print(f"{seconds_to_exit}{'.' * seconds_to_exit}",
                                    color=color)
            Utilities.text_to_speech(number_words[seconds_to_exit - 1])

        self.driver.quit()

    def validate_link(self):
        content = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "themeContent"))
        )
        header = content.text

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
                if self.race() and i + 1 != self.races_to_play:
                    self.new_race()
            self.session.result = True
        except Exception as error:
            Utilities.tts_print("An error has occured", color="red")
            Utilities.colored_print(error, color="white")
            self.session.result = False

        self.session.save_session()
        self.exit()
