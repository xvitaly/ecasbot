# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Union

from ..locales import CommonLocale


class MessagesEn(CommonLocale):
    _messages: Dict[Union[str, str], Union[str, str]] = {
        'as_welcome': 'Add me to supergroup and give me admin rights. I will try to block spammers automatically.',
        'as_alog': 'New user {} ({}) has joined chat {} ({}). Score: {}.',
        'as_restex': 'Cannot restrict a new user with ID {} in chat {} ({}) due to missing admin rights.',
        'as_msgex': 'Exception detected while handling spam message from {} in chat {} ({}).',
        'as_notoken': 'No API token found. Cannot proceed. Forward API token using ENV option and try again!',
        'as_joinhex': 'Failed to handle join message.',
        'as_banned': 'Permanently banned user {} ({}) (score: {}) in chat {} ({}).',
        'as_msgrest': 'Removed message from restricted user {} ({}) in chat {} ({}).',
        'as_amsgrm': 'Admin {} ({}) removed message from user {} ({}) in chat {} ({}).',
        'as_amute': 'Admin {} ({}) muted user {} ({}) in chat {} ({}) until {}.',
        'as_aunres': 'Admin {} ({}) removed all restrictions from user {} ({}) in chat {} ({}).',
        'as_aunban': 'Admin {} ({}) unbanned user {} ({}) in chat {} ({}).',
        'as_aban': 'Admin {} ({}) permanently banned user {} ({}) in chat {} ({}).',
        'as_admerr': 'Failed to handle admin command.',
        'as_chkme': 'Checking of account {} successfully completed. Your score is: {}.',
        'as_pmex': 'Failed to handle command in private chat with bot.',
        'as_repmsg': 'You have a new report from user *{}* ({}) in chat *{}* ({}).\n\nReason: *{}*.\n\nMessage '
                     'link: [click here]({}).',
        'as_repns': 'Cannot send message to admin {} due to Telegram Bot API restrictions.',
        'as_repna': 'Subscribed to events user {} has no more admin rights in chat {} ({}). Watch removed.',
        'as_repsn': 'Sent message to admin {} due to event in chat {} ({}).',
        'as_repex': 'Failed to handle report command.',
        'as_repsub': 'Successfully subscribed to reports in chat {} ({}) .',
        'as_replim': 'I cannot send you direct messages due to API restrictions. PM me first, then try again.',
        'as_repsblg': 'Admin {} ({}) subscribed to events in chat {}.',
        'as_repunsb': 'Successfully unsubscribed from reports in chat {} ({}).',
        'as_repusblg': 'Admin {} ({}) unsubscribed from events in chat {} ({}).',
        'as_repnors': 'No reason specified.',
        'as_replog': 'User {} ({}) reported message of another user {} ({}) in chat {} ({}).',
        'as_leaveok': 'Command successfully executed. Leaving chat {} ({}) now.',
        'as_leavepm': 'You must specify chat ID or username to leave from. Fix this and try again.',
        'as_leavelg': 'Admin {} ({}) asked bot to leave chat {} ({}).',
        'as_swadd': 'Admin {} ({}) added new stopword {} to list.',
        'as_swrem': 'Admin {} ({}) removed stopword {} from list.',
        'as_swuadd': 'New stopword {} added to list.',
        'as_swurem': 'Stopword {} removed from list.',
        'as_swulist': 'Currently restricted words: {}.',
        'as_swerr': 'Failed to add/remove stopword. Try again later.',
        'as_swlist': 'Admin {} ({}) fetched list of stopwords.',
        'as_swpm': 'You must specify a stopword to add/remove. Fix this and try again.',
        'as_entadd': 'Admin {} ({}) added a new entity {} to list.',
        'as_entrem': 'Admin {} ({}) removed entity {} from list.',
        'as_entuadd': 'New entity {} added to list.',
        'as_enturem': 'Entity {} removed from list.',
        'as_entulist': 'Currently restricted entities: {}.',
        'as_enterr': 'Failed to add/remove entity. Try again later.',
        'as_entlist': 'Admin {} ({}) fetched list of restricted entities.',
        'as_entpm': 'You must specify an entity to add/remove. Fix this and try again.',
        'as_leaverr': 'Failed to leave chat {} ({}) due to some error.',
        'as_unathlg': 'User {} ({}) tried to access restricted bot command. Action was denied.',
        'as_pinmsg': 'Admin {} ({}) pinned message {} in chat {} ({}).',
        'as_unpinmsg': 'Admin {} ({}) removed pinned message in chat {} ({}).',
        'as_wipelg': 'Admin {} ({}) removed {} messages (range {}) in chat {} ({}).',
        'as_wipehg': 'Admin {} ({}) tried to remove {} messages in chat {} ({}). Action was denied.',
        'as_wipeerr': 'Failed to delete message with ID {} in chat {} ({}).',
        'as_spamdbg': 'Received message from restricted user {} ({}) in chat {} ({}). Check results: '
                      'entitles: {}, spam: {}, forward: {}.\nContents: {}.',
        'as_crashed': 'The bot has crashed. Scheduling restart in 30 seconds.',
        'as_crashdbg': 'Additional debug information, related to this crash event:',
        'as_resprot': 'Admin {} ({}) tried to restrict protected user {} ({}) in chat {} ({}).',
        'as_banprot': 'Admin {} ({}) tried to ban protected user {} ({}) in chat {} ({}).'
    }
