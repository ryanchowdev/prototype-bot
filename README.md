# Jeff-IX
A multi-purpose Discord bot written in Python 3.  
Note: This project is currently a work-in-progress.  
  
## Running this bot locally
First, make sure you have python3 and python3-pip installed.  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip
```

You must then install the following packages:  
```bash
pip3 install discord.py matplotlib yfinance python-dotenv forex_python pyowm yahoo_fin requests_html
```

To configure the bot, first create a .env file to store your tokens.  
```bash
touch .env
```

Then add the following lines to .env:  
```
DISCORD_TOKEN=<your bot token here>
DISCORD_GUILD='your server name here'
WEATHER_TOKEN=<your OpenWeatherMap token - this is free and required for weather functionality>
```

Now you can run the bot.  
```bash
./bot.py

OR

python3 bot.py
```
