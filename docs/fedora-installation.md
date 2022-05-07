# Installing the bot on Fedora

Get an API token from the [@BotFather](https://t.me/BotFather).

Enable our COPR repository:
```
sudo dnf copr enable xvitaly/ecrepo
```

Install the `ecasbot` package:
```
sudo dnf install ecasbot
```

Open the `/etc/ecasbot-env.conf` configuration file in any text editor and set the value of the `APIKEY` property:
```
sudoedit /etc/ecasbot-env.conf
```

Start the bot and enable its automatic startup:
```
sudo systemctl enable --now ecasbot.service
```
