# About
EasyCoding AntiSpam bot for [Telegram messenger](https://telegram.org/) will block all multimedia messages and links from new users, block chineese bots and users who added them in supergroups.

# License
GNU General Public License version 3. You can find it here: [LICENSE](LICENSE). External libraries can use another licenses, compatible with GNU GPLv3.

# Requirements
 * Python 2.7 or Python 3.x;
 * python-pytelegrambotapi;
 * python-requests.

# Installing bot into Python Virtual Environment
You can also install bot:
 1. Clone this repository:
 ```
 git clone https://github.com/xvitaly/ecasbot.git
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

# Systemd service
 1. Create a new systemd unit `ecasbot.service` in `/lib/systemd/system` directory:

 ```
 [Unit]
 Description=EC AntiSpam bot
 After=network.target
 
 [Service]
 Type=simple
 Restart=always
 RestartSec=30
 User=nobody
 Group=nobody
 ExecStart=VENVPATH/bin/ecasbot
 
 [Install]
 WantedBy=multi-user.target
 ```

 You must change `User` and `Group` and set `VENVPATH` to path of create Python Virtual Environment.
 
 2. Reload system configuration:
 ```
 sudo systemctl daemon-reload
 ```

# Using systemd to control bot

Start bot:
```
sudo systemctl start ecasbot.service
```

Stop bot:
```
sudo systemctl stop ecasbot.service
```

Restart bot:
```
sudo systemctl restart ecasbot.service
```

Enable bot autostart on system boot:
```
sudo systemctl enable ecasbot.service
```

Disable bot autostart on system boot:
```
sudo systemctl disable ecasbot.service
```
