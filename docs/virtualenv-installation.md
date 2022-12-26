# Installing bot into Python Virtual Environment

Clone this repository:
```
git clone https://github.com/xvitaly/ecasbot.git ecasbot
```

Get API token from [@BotFather](https://t.me/BotFather);

Copy configuration file `config/ecasbot.json` to `/etc/ecasbot/ecasbot.json`. You can edit it in any text editor;

Create a new Python Virtual Environment:
```
cd ecasbot
python3 -m venv env
```

Activate Virtual Environment:
```
source env/bin/activate
```

Install bot using Python 3 in VENV:
```

pip3 install .
```

Run installed bot with defined API key:
```bash
APIKEY=API_KEY ecasbot
```
