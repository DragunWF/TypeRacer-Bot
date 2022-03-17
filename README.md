# TypeRacer Bot

## Table of Contents

- [Description](#Description)
- [Functionalities](#Functionalities)
- [Details](#Details)
- [Setup](#Setup)

## Description

Hello, this is an automation project powered by Selenium that allows you to
automate races in [TypeRacer](https://play.typeracer.com/).

## Functionalities

- Automatically logs in to a [typeracer.com](https://play.typeracer.com/) account.
- Automatically plays races. It keeps on playing depending on the settings set by the user.
- Saves each session's stats to `data/sessions.json`.

## Details

- Only works with the **Google Chrome** browser.
- The values for the default settings whenever the bot is started is located
  in `settings.json`.
- Everytime you finish a session whether it's interrupted or not. The stats for
  that session gets saved in `data/sessions.json`.

## Setup

- Firstly, Make sure your [chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and donwload the correct webdriver for you version of chrome.
- Secondly, if you want to try it out. You have to make a file inside the `src`
  directory and make a file named `config.py`. Inside that file, make two variables
  named `username` and `password`. And of course, that's where you'll be storing your
  bot's username and password. **(Please do not use your main)**

```
username = "sample_name"
password = "sample_password"
```

- After that, if you want to override the default settings set for the bot. You can go
  to `data/settings.json` to change the values.

## Contact

- If you want to give me feedback or suggestions on the bot you can contact me via
  discord, my discord tag is **DragonWF#9321**.
