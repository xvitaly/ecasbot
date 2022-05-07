# Controling the bot using systemd

## Creating a systemd unit
Create a new systemd unit `ecasbot.service` in `/lib/systemd/system` directory:

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
EnvironmentFile=/etc/ecasbot

[Install]
WantedBy=multi-user.target
```

You must change `User` and `Group` and set `VENVPATH` to path of create Python Virtual Environment.
 
Copy `config/ecasbot-env.conf` as `/etc/ecasbot`, open it in any text editor and set API token in `APITOKEN` field, received from [@BotFather](https://t.me/BotFather).
 
Reload system configuration:
```
sudo systemctl daemon-reload
```

## Working with systemd

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
