# TypeRacer Bot

## Table of Contents

- [Description](#Description)
- [Functionalities](#Functionalities)
- [Details](#Details)
- [Setup](#Setup)

## Description

This is an automation project powered by Selenium that allows you to
automate races in [TypeRacer](https://play.typeracer.com/).

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

## Setup

- Firstly, Make sure your [chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) is installed and download the correct webdriver for your version of chrome.
- Secondly, if you want to try it out. You have to make a file inside the `src`
  directory and make a file named `config.py`. Inside that file, make two variables
  named `username` and `password`. And of course, that's where you'll be storing your
  bot's username and password. **(Please do not use your main)**

```py
username = "sample_name"
password = "sample_password"
```

- After that, if you want to override the default settings set for the bot. You can go
  to `data/settings.json` to change the values.
- If the bot user you're using hasn't gone through the 100 wpm captcha test. You may
  have to increase the `"key_intervals" values in `data/settings.json` to lower your wpm.

## Status

Currently, most of this bot's main features are complete. There are still some things that
I've been thinking about adding in the future, so it'll still get some updates from time to time.
Just don't expect it to get frequent updates on a consistent time basis.

## Contact

If you want to give me feedback or suggestions on the bot you can contact me via
discord, my discord tag is **DragonWF#9321**.
