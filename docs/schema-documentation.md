# List of options

Available options of the `ecasbot.json` configuration file:

  * `schema` - current schema version;
  * `admins` - the list of the bot admins. This users can execute any bot command and even control super-groups using special bot actions;
  * `restent` - the list of forbidden [entitles](https://core.telegram.org/bots/api#messageentity) for the new users. The bot will remove messages from the restricted users contains any of it;
  * `stopwords` - the list of forbidden words in nicknames of the newly joined users. The bot will score them;
  * `bantime` - user ban time (in seconds). The bot will restrict newly joined users for the specified time;
  * `maxname` - maximum allowed length of the name (both first name and last name). The bot will score users with very long names;
  * `chkrgx` - regular expression for checking user names of the newly joined users in super-groups;
  * `urlrgx` - regular expression for checking if the string contains any URLs. You can get a good one from the [Django project](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45);
  * `logtofile` - log file name including the full path. If not set or empty, stderr will be used;
  * `maxemoji` - the maximum allowed emoji count in messages of the newly joined users. The bot will remove messages exceeding this limit;
  * `nickgoal` - the number of the score points after nickname checks required to block the newly joined user;
  * `msggoal` - the number of the score points after message checks required to delete it;
  * `logfilefmt` - custom formatter for the file logs;
  * `stderrfmt` - custom formatter for the stderr logs;
  * `watches` - the watch list for the reports feature;
  * `restlangs` - the list of restricted languages. The bot will score users using them in their clients;
  * `hidejoins` - enable or disable removing of join messages;
  * `language` - the default language for the logs and the internal messages;
  * `rotatelogs` - use an internal log rotate function (useful for configurations without logrotate.d; recommended for all non-POSIX systems);
  * `duplicatelogs` - allow to duplicate logs to stdout channel when logging to files is enabled;
  * `autoclean` - automatically cleanup used bot commands in super-groups;
  * `restalert` - enable or disable alerting the subscribed admins on new restriction events.
