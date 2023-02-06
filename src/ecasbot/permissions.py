# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from telebot.types import ChatPermissions


class Permissions:
    @property
    def join(self) -> ChatPermissions:
        """
        Return chat permissions for the newly joined users.
        """
        return self.__jp

    @property
    def restrict(self) -> ChatPermissions:
        """
        Return chat permissions for the /restrict command handler.
        """
        return self.__rp

    @property
    def unrestrict(self) -> ChatPermissions:
        """
        Return chat permissions for the /unrestrict command handler.
        """
        return self.__up

    def __init__(self):
        """
        Main constructor of the Permissions class.
        """
        self.__jp = ChatPermissions(can_send_messages=True, can_send_media_messages=False, can_send_audios=False,
                                    can_send_documents=False, can_send_photos=False, can_send_videos=False,
                                    can_send_video_notes=False, can_send_voice_notes=False, can_send_polls=False,
                                    can_send_other_messages=False, can_add_web_page_previews=False,
                                    can_change_info=False, can_invite_users=False, can_pin_messages=False,
                                    can_manage_topics=False)
        self.__rp = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_audios=False,
                                    can_send_documents=False, can_send_photos=False, can_send_videos=False,
                                    can_send_video_notes=False, can_send_voice_notes=False, can_send_polls=False,
                                    can_send_other_messages=False, can_add_web_page_previews=False,
                                    can_change_info=False, can_invite_users=False, can_pin_messages=False,
                                    can_manage_topics=False)
        self.__up = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_audios=True,
                                    can_send_documents=True, can_send_photos=True, can_send_videos=True,
                                    can_send_video_notes=True, can_send_voice_notes=True, can_send_polls=True,
                                    can_send_other_messages=True, can_add_web_page_previews=True, can_change_info=True,
                                    can_invite_users=True, can_pin_messages=True, can_manage_topics=True)
