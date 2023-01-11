# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Union

from ..locales import CommonLocale


class LocaleRu(CommonLocale):
    _messages: Dict[Union[str, str], Union[str, str]] = {
        'as_welcome': 'Добавьте меня в супергруппу и наделите правами администратора. Я буду удалять спам от недавно '
                      'вступивших пользователей полностью автоматически.',
        'as_alog': 'Новый пользователь {} ({}) вступил в чат {} ({}). Баллы: {}.',
        'as_restex': 'Не могу ограничить в правах нового пользователя {} в чате {} ({}) из-за отсутствия прав '
                     'администратора.',
        'as_msgex': 'Во время обработки сообщения от {} в чате {} ({}) произошло исключение.',
        'as_joinhex': 'Не удалось обработать событие входа в чат.',
        'as_banned': 'Пользователь {} ({}) (баллы: {}) был полностью заблокирован в чате {} ({}).',
        'as_msgrest': 'Удалено сообщение от пользователя {} ({}) в чате {} ({}).',
        'as_amsgrm': 'Администратор {} ({}) удалил сообщение пользователя {} ({}) в чате {} ({}).',
        'as_amute': 'Администратор {} ({}) запретил отправлять сообщения пользователю {} ({}) в чате {} ({}) до {}.',
        'as_aunres': 'Администратор {} ({}) снял все ограничения с пользователя {} ({}) в чате {} ({}).',
        'as_aunban': 'Администратор {} ({}) разблокировал пользователя {} ({}) в чате {} ({}).',
        'as_aban': 'Администратор {} ({}) навсегда заблокировал пользователя {} ({}) в чате {} ({}).',
        'as_admerr': 'Не удалось обработать команду администратора.',
        'as_chkme': 'Проверка учётной записи {} успешно завершена. Итоговый балл: {}.',
        'as_pmex': 'Не удалось обработать команду в личных сообщениях с ботом.',
        'as_repmsg': 'Получена новая жалоба от пользователя *{}* ({}) в чате *{}* ({}).\n\nПричина: *{}*.\n\nСсылка '
                     'на сообщение: [нажмите здесь]({}).',
        'as_repns': 'Не могу отправить сообщение администратору {} из-за ограничений Telegram Bot API.',
        'as_repna': 'Подписавшийся на события пользователь {} более не имеет административных прав в чате {} ({}). '
                    'Подписка была аннулирована.',
        'as_repsn': 'Администратору {} было отправлено сообщение из-за новой жалобы в чате {} ({}).',
        'as_repex': 'Не удалось обработать команду отправки жалобы администраторам.',
        'as_repsub': 'Подписка на события в чате {} ({}) была успешно оформлена.',
        'as_replim': 'Не могу отправить вам сообщение из-за ограничений Telegram Bot API. Напишите мне в ЛС, '
                     'после чего повторите попытку.',
        'as_repsblg': 'Администратор {} ({}) подписался на события в чате {}.',
        'as_repunsb': 'Подписка на события в чате {} ({}) была успешно отменена.',
        'as_repusblg': 'Администратор {} ({}) отменил подписку на события в чате {} ({}).',
        'as_repnors': 'Причина не указана.',
        'as_replog': 'Пользователь {} ({}) пожаловался на сообщение другого пользователя {} ({}) в чате {} ({}).',
        'as_leaveok': 'Команда успешно выполнена. Покидаю чат {} ({}) прямо сейчас.',
        'as_leavepm': 'Вы должны указать ID или имя чата, из которого требуется выйти!',
        'as_leavelg': 'Администратор {} ({}) приказал боту покинуть чат {} ({}).',
        'as_swadd': 'Администратор {} ({}) добавил новое запрещённое слово {} в список.',
        'as_swrem': 'Администратор {} ({}) удалил запрещённое слово {} из списка.',
        'as_swuadd': 'Новое запрещённое слово {} добавлено в список.',
        'as_swurem': 'Запрещённое слово {} удалено из списка.',
        'as_swulist': 'Текущий список запрещённых слов: {}.',
        'as_swerr': 'Не удалось добавить/удалить запрещённое слово. Повторите попытку позднее.',
        'as_swlist': 'Администратор {} ({}) запросил вывод списка запрещённых слов.',
        'as_swpm': 'Вы должны указать запрещённое слово, которое требуется добавить в список!',
        'as_entadd': 'Администратор {} ({}) добавил новый тип запрещённого контента {} в список.',
        'as_entrem': 'Администратор {} ({}) удалил тип запрещённого контента {} из списка.',
        'as_entuadd': 'Новый тип запрещённого контента {} добавлен в список.',
        'as_enturem': 'Тип запрещённого контента {} удалён из списка.',
        'as_entulist': 'Текущий список типов запрещённого контента: {}.',
        'as_enterr': 'Не удалось добавить/удалить тип запрещённого контента. Повторите попытку позднее.',
        'as_entlist': 'Администратор {} ({}) запросил вывод списка типов запрещённого контента.',
        'as_entpm': 'Вы должны указать запрещённый тип контента, который требуется добавить в список!',
        'as_leaverr': 'Не удалось покинуть чат {} ({}) из-за возникновения ошибки.',
        'as_unathlg': 'Пользователь {} ({}) пытался получить доступ к ограниченным командам бота. В действии было '
                      'отказано.',
        'as_pinmsg': 'Администратор {} ({}) закрепил сообщение {} в чате {} ({}).',
        'as_unpinmsg': 'Администратор {} ({}) убрал закреплённое сообщение в чате {} ({}).',
        'as_wipelg': 'Администратор {} ({}) удалил {} сообщений (диапазон {}) в чате {} ({}).',
        'as_wipehg': 'Администратор {} ({}) пытался удалить {} сообщений в чате {} ({}). В действии было отказано.',
        'as_wipeerr': 'Произошла ошибка при удалении сообщения с ID {} в чате {} ({}).',
        'as_spamdbg': 'Получено сообщение от ограниченного в правах пользователя {} ({}) в чате {} ({}). Результаты '
                      'проверки: entitles: {}, spam: {}, forward: {}.\nСодержимое сообщения: {}.',
        'as_crashed': 'Бот неожиданно завершил работу из-за следующей ошибки:\n{}.\nИнициирую перезапуск через 30'
                      'секунд.',
        'as_crashdbg': 'Дополнительная отладочная информация, связанная с данным событием:',
        'as_resprot': 'Администратор {} ({}) пытался запретить отправлять сообщения привилегированному пользователю '
                      '{} ({}) в чате {} ({}).',
        'as_banprot': 'Администратор {} ({}) пытался заблокировать привилегированного пользователя {} ({}) в чате {} '
                      '({}).'
    }
