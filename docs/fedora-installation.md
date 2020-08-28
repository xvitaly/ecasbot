# Installing the bot on Fedora

  1. Get an API token from the [@BotFather](https://t.me/BotFather).
  2. Enable our COPR repository:
  ```
  sudo dnf copr enable xvitaly/ecrepo
  ```
  3. Install the `ecasbot` package:
  ```
  sudo dnf install ecasbot
  ```
  4. Open the `/etc/ecasbot-env.conf` configuration file in any text editor and set the value of the `APIKEY` property.
  5. Start the bot and enable its automatic startup:
  ```
  sudo systemctl enable --now ecasbot.service
  ```
