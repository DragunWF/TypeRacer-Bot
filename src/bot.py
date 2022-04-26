import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils


class Bot:
    def __init__(self, username, password, session, settings):
        self.__username = username
        self.__password = password
        self.__session = session

        self.__races_to_play = settings["races"]
        self.__key_intervals = tuple(settings["key_intervals"])
        self.__registered = settings["registered"]
        self.__practice_mode = settings["practice_mode"]

        self.__session.registered = settings["registered"]
        self.__session.practice_mode = settings["practice_mode"]
        self.__session.universe = settings["universe"]

        self.__url = "https://play.typeracer.com/"
        if settings["universe"] != "play":
            self.__url += f"?universe={settings['universe']}"

        if not self.__registered:
            self.__after_restart_races = 0
            self.__restarted = False

        self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver.get(self.__url)

    def __set_guest_username(self):
        usernames = ("Aether", "dancefloor",
                     "Programmer", "Arthur", "SuitAndTie",
                     "To The Moon", "Fly me to the sun",
                     "Excalibur", "King Guest", "Do we exist?")

        sign_in = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        sleep(0.1)

        self.__driver.find_element_by_link_text("Choose a guest nickname (play without an account)").click()
        sleep(2)

        input_username = self.__driver.find_elements_by_class_name("gwt-TextBox")[2]
        input_username.click()
        input_username.clear()
        input_username.send_keys(random.choice(usernames))

        apply = self.__driver.find_elements_by_class_name("gwt-Button")[2]
        apply.click()
        sleep(0.05)

        self.__restarted = False

    def __login(self):
        sign_in = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
        )
        sign_in.click()
        sleep(0.2)

        self.__driver.find_element_by_name("username").send_keys(self.__username)
        self.__driver.find_element_by_name("password").send_keys(self.__password)
        sleep(0.05)

        self.__driver.find_element_by_class_name("gwt-Button").click()
        sleep(1.5)

        self.__driver.get(self.__url)
        sleep(0.1)

    def __enter_race(self):
        link_text = "Practice Yourself" if self.__practice_mode else "Enter a Typing Race"

        start_game = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        start_game.click()
        sleep(0.05)

    def __re_enter_race(self):
        self.__driver.get(self.__url)
        if not self.__registered:
            self.__set_guest_username()
            self.__restarted = True
            self.__after_restart_races = 0
        self.__enter_race()

    def __new_race(self):
        if self.__practice_mode and (self.__session.races <= 1 or self.__restarted):
            close_pop_up = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "OK"))
            )
            close_pop_up.click()
        
        link_text = "New race" if self.__practice_mode else "Race again"
        new_race = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        new_race.click()
        sleep(0.1)

        if not self.__registered and self.__after_restart_races >= 2:
            register_pop_up = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "No thanks :("))
            )
            register_pop_up.click()
            sleep(1)

    def __race(self):
        try:
            input_panel = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inputPanel"))
            )
            race_text = input_panel.text.split("\n")[0]

            if len(race_text) < 1:
                self.__re_enter_race()
                return False

            while True:
                game_time = WebDriverWait(self.__driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "lightLabel"))
                )
                if game_time.text == "Go!":
                    break
                sleep(0.2)
        except:
            self.__re_enter_race()
            return False

        race_input = self.__driver.find_element_by_class_name("txtInput")
        for character in race_text:
            if not self.__driver.find_elements_by_class_name("txtInput-error"):
                race_input.send_keys(character)
                sleep(random.choice(self.__key_intervals))
            else:
                self.__re_enter_race()
                return False
        sleep(0.05)

        if not self.__practice_mode:
            race_status = self.__driver.find_element_by_class_name(
                "gameStatusLabel")
            if race_status.text == "You finished 1st!":
                Utils.colored_print(race_status.text, color="cyan")
                self.__session.wins += 1
            else:
                Utils.colored_print(race_status.text, color="yellow")
                self.__session.losses += 1

        if not self.__registered:
            self.__after_restart_races += 1

        self.__session.races += 1
        sleep(0.1)

        return True

    def __exit(self):
        Utils.tts_print("Shutting down in...", color="yellow")

        number_words = ("one", "two", "three")
        for i in range(3):
            seconds_to_exit = 4 - (i + 1)
            Utils.colored_print(f"{seconds_to_exit}{'.' * seconds_to_exit}",
                                    color="yellow")
            Utils.text_to_speech(number_words[seconds_to_exit - 1])

        self.__driver.quit()

    def __validate_link(self):
        content = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "themeContent"))
        )
        header = content.text

        if header == "This URL was not recognized":
            Utils.tts_print("Make sure to put a valid universe URL next time.",
                                color="yellow")
            raise Exception("Invalid universe input")

    def run(self):
        try:
            self.__validate_link()
            self.__login() if self.__registered else self.__set_guest_username()
            self.__enter_race()

            for i in range(self.__races_to_play):
                Utils.colored_print(f"Session Race Count: {i + 1}",
                                        color="green")
                if self.__race() and i + 1 != self.__races_to_play:
                    self.__new_race()
            self.__session.result = True
        except Exception as error:
            Utils.tts_print("An error has occured!", color="red")
            print(f"ERROR: {error}")
            self.__session.result = False

        self.__session.save_session()
        self.__exit()
