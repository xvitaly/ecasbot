# Installing bot into Python Virtual Environment
You can also install bot:
 1. Clone this repository:
 ```
 git clone https://github.com/xvitaly/ecasbot.git ecasbot
 ```
 2. Get API tokens from [@BotFather](https://t.me/BotFather), open `ecasbot/settings.py` file in any text editor and set it.
 3. Create a new Python Virtual Environment:
 ```
 python3 -m venv ecasbot
 ```
 4. Activate Virtual Environment:
 ```
 source ecasbot/bin/activate
 ```
 5. Install dependencies for bot:
 ```
 pip3 install pyTelegramBotAPI
 ```
 6. Install bot using Python 3 in VENV:
 ```
 cd ecasbot
 python3 setup.py install
 ```
 6. Run installed bot:
 ```bash
 /bin/ecasbot
 ```
