# List of available bot actions

## Allowed users

Bot will allow to use basic admin features in supergroups for:

 * creator of supergroup;
 * admins of supergroup;
 * any users from `admins` setting of configuration file.

## Basic admin actions

List of currently supported admin actions in supergroups:

 * `/remove` or `/rm` (replies) - remove specified message;
 * `/wipe RANGE` (direct) - remove messages from specified range (will return an error if the range is greater than 50);
 * `/ban` or `/block` (replies) - permanently block author of specified message in supergroup;
 * `/restrict` or `/mute` (replies) - permanently restrict author of specified message in supergroup;
 * `/restrict DAYS` or `/mute DAYS` (replies) - restrict author of specified message in supergroup for specified number of days;
 * `/unrestrict` or `/un` (replies) - remove all restrictions from author of specified message in supergroup;
 * `/unban ID` (direct) - remove all restrictions from author specified Telegram user ID in supergroup;
 * `/subscribe` (direct) - subscribe to all user reports issued in supergroup;
 * `/unsubscribe` (direct) - unsubscribe from all user reports issued in supergroup;
 * `/pin` (replies) - pin specified message in supergroup;
 * `/unpin` (direct) - unpin all messages from supergroup.

## Advanced admin actions

This actions can be executed only by bot owners and admins specified in `admins` setting of configuration file.

List of currently supported advanced admin actions:

 * `/leave CHAT_ID` (private messages only) - force bot to leave chat specified in `CHAT_ID` parameter;
 * `/sw_add WORD` (private messages only) - add a new stopword `WORD` to the list of restricted words for new users;
 * `/sw_remove WORD` (private messages only) - remove stopword `WORD` from the list of restricted words for new users;
 * `/sw_list` (private messages only) - show all restricted words for new users.

## User actions

List of currently supported user actions:

 * `/report` or `/report REASON` (replies) - report specified message to admins (with optional reason);
 * `/checkme` (private messages only) - check user profile and show current score for debug purposes.
