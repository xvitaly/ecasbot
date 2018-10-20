# Installing bot into Python Virtual Environment
You can also install bot:
 1. Clone this repository:
 ```
 git clone https://github.com/xvitaly/ecasbot.git ecasbot
 ```
 2. Get API tokens from [@BotFather](https://t.me/BotFather);
 3. Copy configuration file `config/ecasbot.json` to `/etc/ecasbot/ecasbot.json`, open it in any text editor and set it API token;
 4. Create a new Python Virtual Environment:
 ```
 python3 -m venv ecasbot
 ```
 5. Activate Virtual Environment:
 ```
 source ecasbot/bin/activate
 ```
 6. Install bot using Python 3 in VENV:
 ```
 cd ecasbot
 python3 setup.py install
 ```
 7. Run installed bot:
 ```bash
 /bin/ecasbot
 ```
