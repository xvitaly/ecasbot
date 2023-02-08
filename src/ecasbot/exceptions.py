# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

__all__ = ['ConfigNotFound', 'TokenNotFound', 'WrongSchemaVersion']


class ConfigNotFound(Exception):
    """
    Base class for the missing JSON config file errors.
    """


class TokenNotFound(Exception):
    """
    Base class for the missing Telegram Bot API token errors.
    """


class WrongSchemaVersion(Exception):
    """
    Base class for the inccorrect JSON config file schema
    version errors.
    """
