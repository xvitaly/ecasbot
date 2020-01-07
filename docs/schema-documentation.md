# List of options

Available options of `acasbot.json` configuration file:

 * `schema` - current schema version;
 * `admins` - list of bot admins. This users can execute any bot command and even control super-groups using special bot actions;
 * `restent` - list of forbidden [entitles](https://core.telegram.org/bots/api#messageentity) for new users. Bot will remove messages from restricted users contains any of it;
 * `stopwords` - list of forbidden words in nicknames of newly joined users. Bot will score them;
 * `bantime` - user ban time (in seconds). Bot will restrict newly joined users for this time;
 * `maxname` - maximum allowed length of name (both first name and last name). Bot will score users with very long names;
 * `chkrgx` - regular expression for checking user names of newly joined users in super-groups;
 * `urlrgx` - regular expression for checking if string contains any URLs. You can get a good one from [Django project](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45);
 * `logtofile` - log file name with full path. If not set or empty, stderr will be used;
 * `maxemoji` - maximum allowed emoji count in messages of new users. Bot will remove messages exceeding this limit;
 * `nickgoal` - number of score points after nickname checks required to block new joined user;
 * `msggoal` - number of score points after message checks required to delete it;
 * `logfilefmt` - custom formatter for file logs;
 * `stderrfmt` - custom formatter for stderr logs;
 * `watches` - watch list for reports feature;
 * `restlangs` - list of restricted languages. Bot will score users using them in their clients;
 * `hidejoins` - enable or disable join messages removing.

# Schema changes

## From 7 to 8
Field `hidejoins` added. Default value it `true`.

## From 7 to 8
Field `tgkey` removed. Environment option `APIKEY` should be used.

## From 6 to 7
Field `watchlist` renamed to `watches` due to major changes in API and format.
