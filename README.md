## AutoRegion Telegram Bot

This Telegram bot is based on a code that was described in the amazing 
article written by **Arez Khalimi** [How to Create and Deploy a Telegram Bot?](https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/).
From this code I've changed Bottle WSGI micro web-framework to Flask, and added my own REST API. Another useful article is [I built a serverless Telegram bot over the weekend. Here’s what I learned](https://medium.freecodecamp.org/how-to-build-a-server-less-telegram-bot-227f842f4706) by **Moses Soh**.

The bot, available at `@autoregion_bot` (for instance, [https://web.telegram.org/#/im?p=@autoregion_bot](https://web.telegram.org/#/im?p=@autoregion_bot)), 
receive vehicle registration plate region code (or part of the code) of a selected country and retrieve the corresponding municipality and cities in it. 
For now it supports only serbian region codes (see [wiki](https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Serbia)), both Latin and Cyrillic, and Serbian and Russian languages.

## Installation

1. Clone this repository and go to the folder:

```
git clone https://github.com/luberlinder/telegram-autoregion-bot.git
cd telegram-autoregion-bot
```

2. Create `config.ini` that is used by `settings.py` with settings like this:

```INI
[Credentials]
TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
APP_URL=https://<PROJECT_ID>.appspot.com

[Settings]
API_URL=http://209.97.149.9:3000/api/
BOT_URL=https://api.telegram.org/bot
```
- TOKEN: you should get it from Telegram's BotFather (see the Khalimi's article).
- PROJECT_ID: your project ID that you'll choose on the next step by `gcloud projects create <PROJECT_ID>` command.
- API_URL: it's my REST API address on Digital Ocean and it won't be active forever. Change it to your own API if you have one.

3. Deploy the project to Google Cloud Platfrom (or Heroku, or whatever that have SSL/TLS):

```
gcloud projects create <PROJECT_ID>
gcloud app create --region=<REGION>
gcloud app deploy
```

`gcloud app deploy` automaticaly will:

- create runtime environment described in `app.yaml` (Python 3.7),
- install dependencies listed in `requirements.txt` (latest Flask and Requests), 
- connect this web application to google's gunicorn because of name convention: `main.py` and `app` instance in it,
- set cron jobs configured in `cron.yaml` (setting webhook every day).

## Usage

1. Find the bot on Telegram: `@autoregion_bot` or your own name, created in Telegram's BotFather.
2. Start the conversation: `/start`
3. Type searching code: 
    - **BG**
    - or just: **r**
    - Cyrillic also supported: **ш**
4. See which it region is: 
    - BG: Белград (Бараево, Вождовац, Врачар, Гроцка, Звездара, Земун, Лазаревац, Младеновац, Нови-Београд, Обреновац, Палилула, Раковица, Савски-Венац, Сопот, Стари-Град, Сурчин, Чукарица)
    - RA: Рашка (Рашка)\
      RU: Рума (Ириг, Печинци, Рума)
    - ША: Шабац (Владимирци, Коцелева, Шабац)\
      ШИ: Шид (Шид)

