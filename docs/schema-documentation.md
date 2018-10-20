List of options
==============================

Available options of `acasbot.json` configuration file:

 * `schema` - current schema version;
 * `tgkey` - Telegram Bot API key. Can be obtained from [@BotFather](https://t.me/BotFather);
 * `admins` - list of bot admins. This users can execute any bot command and even control supergroups using special bot actions;
 * `restent` - list of forbidden [entitles](https://core.telegram.org/bots/api#messageentity) for new users. Bot will remove any messages from restricted users contains any of it;
 * `stopwords` - list of forbidden words in nicknames of new users. Bot will score such users;
 * `bantime` - user ban time (in seconds). Bot will restrict new users for this time;
 * `maxname` - maximum allowed length of name. Bot will score users with very long names;
 * `chkrgx` - regular expression for checking user names on joining supergroups;
 * `urlrgx` - regular expression for checking if string contains any URLs. You can get a good one from [Django project](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45);
 * `logtofile` - log file name with full path. If not set or empty, stderr will be used;
 * `maxemoji` - maximum allowed emoji count in messages of new users. Bot will remove messages exceeding this limit;
 * `nickgoal` - number of score points after nickname checks required to block new joined user;
 * `msggoal` - number of score points after message checks required to delete it;
 * `logfilefmt` - custom formatter for file logs;
 * `stderrfmt` - custom formatter for stderr logs;
 * `watches` - watch list for reports feature;
 * `restlangs` - list of restricted languages. Bot will score users using them in their clients.
