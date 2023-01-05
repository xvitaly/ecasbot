% ecasbot(1) | General Commands Manual

# NAME

ecasbot - EC AntiSpam bot for the Telegram messenger 

# SYNOPSIS

**ecasbot**

# DESCRIPTION

EC AntiSpam bot for the Telegram messenger will automatically detect and block multimedia messages, links from the newly joined users, some common spam bots and users who added them to super-groups.

# BOT ACTIONS

EC AntiSpam bot can be controlled via Telegram messages.

## Allowed users

Bot will allow to use basic admin features in supergroups for:

  * creator of the supergroup;
  * admins of the supergroup;
  * any users from the **admins** setting of the configuration file.

## Basic admin actions

List of currently supported admin actions for supergroups:

  * **/remove** or **/rm** (replies) - remove the specified message;
  * **/wipe RANGE** (direct) - remove messages from the specified range (will return an error if the range is greater than 50);
  * **/ban** or **/block** (replies) - permanently block the author of the specified message in the supergroup;
  * **/restrict** or **/mute** (replies) - permanently restrict the author of the specified message in the supergroup;
  * **/restrict DAYS** or **/mute DAYS** (replies) - restrict the author of the specified message in the supergroup for the specified number of days;
  * **/unrestrict** or **/un** (replies) - remove all restrictions from the author of the specified message in the supergroup;
  * **/unban ID** (direct) - remove all restrictions from the author of the specified Telegram user ID in the supergroup;
  * **/subscribe** (direct) - subscribe to all user reports issued in the supergroup;
  * **/unsubscribe** (direct) - unsubscribe from all user reports issued in the supergroup;
  * **/pin** (replies) - pin the specified message in the supergroup;
  * **/unpin** (direct) - unpin all messages from the supergroup.

## Advanced admin actions

This actions can be executed only by bot owners and admins specified in the **admins** setting of the configuration file.

List of currently supported advanced admin actions:

  * **/leave CHAT_ID** (private messages only) - force the bot to leave the chat specified in the **CHAT_ID** parameter;
  * **/sw_add WORD** (private messages only) - add a new stopword **WORD** to the list of restricted words for the new users;
  * **/sw_remove WORD** (private messages only) - remove stopword **WORD** from the list of restricted words for the new users;
  * **/sw_list** (private messages only) - show the list of restricted words for the new users;
  * **/ent_add ENTITY** (private messages only) - add a new entity **ENTITY** to the list of restricted entities for the new users;
  * **/ent_remove ENTITY** (private messages only) - remove entity **ENTITY** from the list of restricted entities for the new users;
  * **/ent_list** (private messages only) - show the list of restricted entities for the new users.

## User actions

List of currently supported user actions:

  * **/report** or **/report REASON** (replies) - report the specified message to admins (with optional reason);
  * **/checkme** (private messages only) - check user profile and show current score for the debug purposes.

# ENVIRONMENT OPTIONS

ecasbot support of getting options from environment variables.

## Supported options

  * **APIKEY** - API token from the [\@BotFather](https://t.me/BotFather);
  * **CFGPATH** - override the default directory for the configuration files. If not set - **/etc/ecasbot** will be used on \*nix OS and **%APPDATA%/ecasbot** on Windows;
  * **LOGLEVEL** - specify current logging level. If not set - **INFO** will be used.

## Forwarding options

Export environment options using `export` command:

```
export APIKEY=ABCDEFG0123456
export CFGPATH=/etc/ecasbot
export LOGLEVEL=INFO
```

Start application:

```
ecasbot
```

# CONFIGURATION FILES

Available options of the `ecasbot.json` configuration file:

  * **schema** - current schema version;
  * **admins** - the list of the bot admins. This users can execute any bot command and even control super-groups using special bot actions;
  * **restent** - the list of forbidden [entitles](https://core.telegram.org/bots/api#messageentity) for the new users. The bot will remove messages from the restricted users contains any of it;
  * **stopwords** - the list of forbidden words in nicknames of the newly joined users. The bot will score them;
  * **bantime** - user ban time (in seconds). The bot will restrict newly joined users for the specified time;
  * **maxname** - maximum allowed length of the name (both first name and last name). The bot will score users with very long names;
  * **chkrgx** - regular expression for checking user names of the newly joined users in super-groups;
  * **urlrgx** - regular expression for checking if the string contains any URLs. You can get a good one from the [Django project](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45);
  * **logtofile** - log file name including the full path. If not set or empty, stderr will be used;
  * **maxemoji** - the maximum allowed emoji count in messages of the newly joined users. The bot will remove messages exceeding this limit;
  * **nickgoal** - the number of the score points after nickname checks required to block the newly joined user;
  * **msggoal** - the number of the score points after message checks required to delete it;
  * **logfilefmt** - custom formatter for the file logs;
  * **stderrfmt** - custom formatter for the stderr logs;
  * **watches** - the watch list for the reports feature;
  * **restlangs** - the list of restricted languages. The bot will score users using them in their clients;
  * **hidejoins** - enable or disable removing of join messages;
  * **language** - the default language for the logs and the internal messages;
  * **rotatelogs** - use an internal log rotate function (useful for configurations without logrotate.d; recommended for all non-POSIX systems);
  * **duplicatelogs** - allow to duplicate logs to stdout channel when logging to files is enabled.

# SYSTEMD UNIT

After installation, the systemd-unit **ecasbot.service** will be added.

## Changing settings

Launcher configuration, including mandatory Telegram API key, stored in **/etc/ecasbot/ecasbot-env.conf**. It uses standard key-value syntax.

Bot settings are stored in the **/etc/ecasbot/ecasbot.json** configuration file. It uses JSON syntax.

## Enabling unit

Enable systemd-unit and run it on system startup:

```
sudo systemctl enable --now ecasbot.service
```

## Disabling unit

Disable systemd-unit and stop runing it on system startup:

```
sudo systemctl disable ecasbot.service
```

## Running unit

You can also run systemd-unit without adding it to startup.

Start EC AntiSpam Bot:

```
sudo systemctl start ecasbot.service
```

Stop EC AntiSpam Bot:

```
sudo systemctl stop ecasbot.service
```

# AUTHORS

Copyright (c) 2017-2023 EasyCoding Team.
