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
