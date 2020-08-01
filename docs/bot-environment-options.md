# List of environment options

Available environment options:

  * `APIKEY` - API token from the [@BotFather](https://t.me/BotFather);
  * `CFGPATH` - override the default directory for the [configuration files](schema-documentation.md). If not set `/etc/ecasbot` will be used on *nix OS and `%APPDATA%/ecasbot` on Windows;
  * `LOGLEVEL` - specify current logging level. If not set `INFO` will be used;
  * `ROTATE_LOGS` - use an internal log rotate function (useful for configurations without logrotate.d; always enabled on all non-POSIX systems).
