# TypeRacer Bot

![GitHub top language](https://img.shields.io/github/languages/top/DragunWF/TypeRacer-Bot)
![Lines of code](https://img.shields.io/tokei/lines/github/DragunWF/TypeRacer-Bot)
![GitHub repo size](https://img.shields.io/github/repo-size/DragunWF/TypeRacer-Bot)

## Table of Contents

- [Description](#Description)
- [Functionalities](#Functionalities)
- [Details](#Details)
- [Setup](#Setup)
- [Status](#Status)
- [Contact](#Contact)

## Description

This is an automation project powered by Selenium that allows you to
automate races in [TypeRacer](https://play.typeracer.com/). Just sit back
and relax while observing the bot doing its work.

## Functionalities

- Automatically logs in to a [typeracer.com](https://play.typeracer.com/) account.
- Automatically plays races. It keeps on playing depending on the settings set by the user.
- Saves each session's stats and details to `data/sessions.json`.

## Details

- Only works with the **Google Chrome** browser.
- The values for the default settings whenever the bot is started is located
  in `settings.json`.
- Every time you finish a session whether it's interrupted or not. The stats for
  that session gets saved in `data/sessions.json`.
- The bot can only type around 90-95 wpm because going over 100 wpm will result in
  the website giving you a captcha test.

## Setup

- Make sure your [chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  is installed and download the correct webdriver for your version of chrome.
- **if you're only playing as a guest user then you can just go ahead and run `main.py` to get started immediately.**
- if you want to try it out with a registered bot account. You have to go to `data/settings.json`
  and set `registered` to `true` and of course, you have to enter your bot's details at `"username"`
  and `"password"`. Then after that you can just run `main.py` to get started.

```json
[
  {
    "registered": false,
    "practice_mode": false,
    "races": 250,
    "universe": "play",
    "key_intervals": [0.065, 0.07, 0.075, 0.08, 0.085]
  },
  {
    "username": "sample_username",
    "password": "sample_password"
  }
]
```

- **Warning** for people wanting to use it with a registered account: it's possible you can get
  banned from typeracer depending on what you do, so use it at your own risk.
- if you want to override the default settings set for the bot. You can go to
  `data/settings.json` to change the values.

## Status

Currently, this bot's main features are complete. There are still some extra things I've
been thinking about adding in the future, so it'll still get some updates from time to time.
Just don't expect it to get frequent updates on a consistent time basis.

## Contact

If you want to give me feedback or suggestions on the bot you can contact me via
discord, my discord tag is **DragonWF#9321**.
