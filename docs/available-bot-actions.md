# List of available bot actions

## Allowed users

Bot will allow to use basic admin features in supergroups for:

  * creator of the supergroup;
  * admins of the supergroup;
  * any users from the `admins` setting of the [configuration file](schema-documentation.md).

## Basic admin actions

List of currently supported admin actions for supergroups:

  * `/remove` or `/rm` (replies) - remove the specified message;
  * `/wipe RANGE` (direct) - remove messages from the specified range (will return an error if the range is greater than 50);
  * `/ban` or `/block` (replies) - permanently block the author of the specified message in the supergroup;
  * `/restrict` or `/mute` (replies) - permanently restrict the author of the specified message in the supergroup;
  * `/restrict DAYS` or `/mute DAYS` (replies) - restrict the author of the specified message in the supergroup for the specified number of days;
  * `/unrestrict` or `/un` (replies) - remove all restrictions from the author of the specified message in the supergroup;
  * `/unban ID` (direct) - remove all restrictions from the author of the specified Telegram user ID in the supergroup;
  * `/subscribe` (direct) - subscribe to all user reports issued in the supergroup;
  * `/unsubscribe` (direct) - unsubscribe from all user reports issued in the supergroup;
  * `/pin` (replies) - pin the specified message in the supergroup;
  * `/unpin` (direct) - unpin all messages from the supergroup.

## Advanced admin actions

This actions can be executed only by bot owners and admins specified in the `admins` setting of the configuration file.

List of currently supported advanced admin actions:

  * `/leave CHAT_ID` (private messages only) - force the bot to leave the chat specified in the `CHAT_ID` parameter;
  * `/sw_add WORD` (private messages only) - add a new stopword `WORD` to the list of restricted words for the new users;
  * `/sw_remove WORD` (private messages only) - remove stopword `WORD` from the list of restricted words for the new users;
  * `/sw_list` (private messages only) - show the list of restricted words for the new users;
  * `/ent_add ENTITY` (private messages only) - add a new entity `ENTITY` to the list of restricted entities for the new users;
  * `/ent_remove ENTITY` (private messages only) - remove entity `ENTITY` from the list of restricted entities for the new users;
  * `/ent_list` (private messages only) - show the list of restricted entities for the new users.

## User actions

List of currently supported user actions:

  * `/report` or `/report REASON` (replies) - report the specified message to admins (with optional reason);
  * `/checkme` (private messages only) - check user profile and show current score for the debug purposes.
