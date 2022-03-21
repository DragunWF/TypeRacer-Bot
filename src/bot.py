import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utilities


class Bot:
    def __init__(self, username, password, session, settings):
        self.username = username
        self.password = password
        self.session = session

        self.races_to_play = settings["races"]
        self.key_intervals = tuple(settings["key_intervals"])
        self.registered = settings["registered"]
        self.practice_mode = settings["practice_mode"]

        self.session.registered = settings["registered"]
        self.session.practice_mode = settings["practice_mode"]
        self.session.universe = settings["universe"]

        self.url = "https://play.typeracer.com/"
        if settings["universe"] != "play":
            self.url += f"?universe={settings['universe']}"

        if not self.registered:
            self.restarted = False

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)

    def set_guest_username(self):
        usernames = ("Aether", "dancefloor",
                     "Programmer", "Arthur", "SuitAndTie",
                     "To The Moon", "Fly me to the sun",
                     "Excalibur", "King Guest", "Do we exist?")

        sign_in = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        sleep(0.1)

        self.driver.find_element_by_link_text("Choose a guest nickname (play without an account)").click()
        sleep(2)

        input_username = self.driver.find_elements_by_class_name("gwt-TextBox")[2]
        input_username.click()
        input_username.clear()
        input_username.send_keys(random.choice(usernames))

        apply = self.driver.find_elements_by_class_name("gwt-Button")[2]
        apply.click()
        sleep(0.05)

        self.restarted = False

    def login(self):
        sign_in = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        sleep(0.2)

        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
        sleep(0.05)

        self.driver.find_element_by_class_name("gwt-Button").click()
        sleep(1.5)

        self.driver.get(self.url)
        sleep(0.1)

    def enter_race(self):
        link_text = "Practice Yourself" if self.practice_mode else "Enter a Typing Race"

        start_game = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        start_game.click()
        sleep(0.05)

    def re_enter_race(self):
        self.driver.get(self.url)
        if not self.registered:
            self.set_guest_username()
            self.restarted = True
        self.enter_race()

    def new_race(self):
        if self.practice_mode and (self.session.races <= 1 or self.restarted):
            close_pop_up = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "OK"))
            )
            close_pop_up.click()

        link_text = "New race" if self.practice_mode else "Race again"
        new_race = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        new_race.click()
        sleep(0.1)

    def race(self):
        try:
            input_panel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inputPanel"))
            )
            race_text = input_panel.text.split("\n")[0]

            if len(race_text) < 1:
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
        except:
            self.re_enter_race()
            return False

        race_input = self.driver.find_element_by_class_name("txtInput")
        for character in race_text:
            if not self.driver.find_elements_by_class_name("txtInput-error"):
                race_input.send_keys(character)
                sleep(random.choice(self.key_intervals))
            else:
                self.re_enter_race()
                return False
        sleep(0.05)

        if not self.practice_mode:
            race_status = self.driver.find_element_by_class_name(
                "gameStatusLabel")
            if race_status.text == "You finished 1st!":
                Utilities.colored_print(race_status.text, color="cyan")
                self.session.wins += 1
            else:
                Utilities.colored_print(race_status.text, color="yellow")
                self.session.losses += 1

        self.session.races += 1
        sleep(0.1)

        return True

    def exit(self):
        Utilities.tts_print("Shutting down in...", color="yellow")

        number_words = ("one", "two", "three")
        for i in range(3):
            seconds_to_exit = 4 - (i + 1)
            Utilities.colored_print(f"{seconds_to_exit}{'.' * seconds_to_exit}",
                                    color="yellow")
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
            self.login() if self.registered else self.set_guest_username()
            self.enter_race()
            for i in range(self.races_to_play):
                Utilities.colored_print(f"Session Race Count: {i + 1}",
                                        color="green")
                if self.race() and i + 1 != self.races_to_play:
                    self.new_race()
            self.session.result = True
        except Exception as error:
            Utilities.tts_print("An error has occured!", color="red")
            print(f"ERROR: {error}")
            self.session.result = False

        self.session.save_session()
        self.exit()
