# coding=utf-8

# EC AntiSpam bot for Telegram Messenger
# Copyright (c) 2017 - 2020 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, Union

from ..locales import CommonLocale


class MessagesRu(CommonLocale):
    _messages: Dict[Union[str, str], Union[str, str]] = {
        'as_welcome': 'Добавьте меня в супергруппу и наделите правами администратора. Я буду удалять спам от недавно '
                      'вступивших пользователей полностью автоматически.',
        'as_alog': 'Новый пользователь {} ({}) вступил в чат {} ({}). Баллы: {}.',
        'as_restex': 'Не могу ограничить в правах нового пользователя {} в чате {} ({}) из-за отсутствия прав '
                     'администратора.',
        'as_msgex': 'Во время обработки сообщения от {} в чате {} ({}) произошло исключение.',
        'as_notoken': 'Не указан API токен для бота. Пожалуйста, передайте его при помощи переменных окружения и '
                      'перезапустите.',
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
        'as_leaverr': 'Не удалось покинуть чат {} ({}) из-за возникновения ошибки.',
        'as_unath': 'У вас нет прав для доступа к данной команде ввиду отсутствия прав администратора. О данном '
                    'инциденте будет доложено администраторам чата.',
        'as_unathlg': 'Пользователь {} ({}) пытался получить доступ к ограниченным командам бота. В действии было '
                      'отказано.',
        'as_pinmsg': 'Администратор {} ({}) закрепил сообщение {} в чате {} ({}).',
        'as_unpinmsg': 'Администратор {} ({}) убрал закреплённое сообщение в чате {} ({}).',
        'as_wipelg': 'Администратор {} ({}) удалил {} сообщений (диапазон {}) в чате {} ({}).',
        'as_wipehg': 'Администратор {} ({}) пытался удалить {} сообщений в чате {} ({}). В действии было отказано.',
        'as_spamdbg': 'Получено сообщение от ограниченного в правах пользователя {} ({}) в чате {} ({}). Результаты '
                      'проверки: entitles: {}, spam: {}, forward: {}.\nСодержимое сообщения: {}.',
        'as_crashed': 'Бот неожиданно завершил работу. Инициирую перезапуск через 30 секунд.',
        'as_crashdbg': 'Дополнительная отладочная информация, связанная с данным событием:',
        'as_resprot': 'Администратор {} ({}) пытался запретить отправлять сообщения привилегированному пользователю '
                      '{} ({}) в чате {} ({}).',
        'as_banprot': 'Администратор {} ({}) пытался заблокировать привилегированного пользователя {} ({}) в чате {} '
                      '({}).'
    }
