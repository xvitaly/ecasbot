# EC AntiSpam bot

[![GitHub version](https://badge.fury.io/gh/xvitaly%2Fecasbot.svg)](https://github.com/xvitaly/ecasbot/releases)
[![Github downloads](https://img.shields.io/github/downloads/xvitaly/ecasbot/total.svg?label=GH%20downloads&maxAge=60)](https://github.com/xvitaly/ecasbot/releases)
[![Build status](https://travis-ci.org/xvitaly/ecasbot.svg?branch=master)](https://travis-ci.org/xvitaly/ecasbot)
[![GitHub issues](https://img.shields.io/github/issues/xvitaly/ecasbot.svg?label=issues&maxAge=60)](https://github.com/xvitaly/ecasbot/issues)
---

EC AntiSpam bot for [Telegram](https://telegram.org/) messenger will block all multimedia messages and links from new users, some common spam bots and users who added them to super-groups.

# License
GNU General Public License version 3. You can find it here: [LICENSE](LICENSE). External libraries can use another licenses, compatible with GNU GPLv3.

# Requirements
 * Python 2.7 or Python 3.x;
 * python-pytelegrambotapi;
 * python-requests.

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
