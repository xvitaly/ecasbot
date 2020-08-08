# List of options

Available options of the `acasbot.json` configuration file:

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
 * `rotatelogs` - use an internal log rotate function (useful for configurations without logrotate.d; always enabled on all non-POSIX systems).

# Schema changes

## From 10 to 11
The field `rotatelogs` was added. The default value is `false`.

## From 9 to 10
The field `language` was added. The default value is `en`.

## From 8 to 9
The field `hidejoins` was added. The default value is `true`.

## From 7 to 8
The field `tgkey` was removed. The environment option `APIKEY` should be used.

## From 6 to 7
The field `watchlist` renamed to `watches` due to major changes in API and format.
