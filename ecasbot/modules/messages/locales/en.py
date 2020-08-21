# coding=utf-8

# EC AntiSpam bot for the Telegram messenger
# Copyright (c) 2017 - 2020 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
        'as_leaverr': 'Failed to leave chat {} ({}) due to some error.',
        'as_unath': 'You cannot access this command due to missing admin rights. This issue will be reported.',
        'as_unathlg': 'User {} ({}) tried to access restricted bot command. Action was denied.',
        'as_pinmsg': 'Admin {} ({}) pinned message {} in chat {} ({}).',
        'as_unpinmsg': 'Admin {} ({}) removed pinned message in chat {} ({}).',
        'as_wipelg': 'Admin {} ({}) removed {} messages (range {}) in chat {} ({}).',
        'as_wipehg': 'Admin {} ({}) tried to remove {} messages in chat {} ({}). Action was denied.',
        'as_spamdbg': 'Received message from restricted user {} ({}) in chat {} ({}). Check results: '
                      'entitles: {}, spam: {}, forward: {}.\nContents: {}.',
        'as_crashed': 'The bot has crashed. Scheduling restart in 30 seconds.',
        'as_crashdbg': 'Additional debug information, related to this crash event:',
        'as_resprot': 'Admin {} ({}) tried to restrict protected user {} ({}) in chat {} ({}).',
        'as_banprot': 'Admin {} ({}) tried to ban protected user {} ({}) in chat {} ({}).'
    }
