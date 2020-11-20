# EC AntiSpam bot

[![GitHub version](https://img.shields.io/github/v/release/xvitaly/ecasbot?sort=semver&color=brightgreen&logo=git&logoColor=white)](https://github.com/xvitaly/ecasbot/releases)
[![PyPi Version](https://img.shields.io/pypi/v/ecasbot.svg?logo=pypi&logoColor=white)](https://pypi.org/project/ecasbot/)
[![GitHub CI status](https://github.com/xvitaly/ecasbot/workflows/Python%20CI/badge.svg?branch=dev)](https://github.com/xvitaly/ecasbot/actions)
[![AppVeyor status](https://ci.appveyor.com/api/projects/status/tcanemsupba2q64u?svg=true)](https://ci.appveyor.com/project/xvitaly/ecasbot)
[![COPR status](https://copr.fedorainfracloud.org/coprs/xvitaly/ecrepo/package/ecasbot/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/xvitaly/ecrepo/package/ecasbot/)
[![LGTM grade](https://img.shields.io/lgtm/grade/python/g/xvitaly/ecasbot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xvitaly/ecasbot/context:python)
[![LGTM alerts](https://img.shields.io/lgtm/alerts/g/xvitaly/ecasbot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xvitaly/ecasbot/alerts/)
[![CodeFactor](https://www.codefactor.io/repository/github/xvitaly/ecasbot/badge/dev)](https://www.codefactor.io/repository/github/xvitaly/ecasbot/overview/dev)
[![GitHub issues](https://img.shields.io/github/issues/xvitaly/ecasbot.svg?label=issues)](https://github.com/xvitaly/ecasbot/issues)
---

EC AntiSpam bot for the [Telegram](https://telegram.org/) messenger will automatically detect and block multimedia messages, links from the newly joined users, some common spam bots and users who added them to super-groups.

Warning! Do not use `dev` branch in production due to lots of breaking changes. Use `master` or `stable` instead.

# License
GNU General Public License version 3. You can find it here: [LICENSE](LICENSE). External libraries can use another licenses, compatible with GNU GPLv3.

Icon for the Windows executable and installer by [Chris Banks](https://www.deviantart.com/chrisbanks2), licensed under the terms of the [CC Attribution Non-Commercial](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

# Requirements
  * Python 3.6+;
  * [python-pytelegrambotapi](https://github.com/eternnoir/pyTelegramBotAPI);
  * [python-requests](https://github.com/requests/requests);
  * [python-six](https://github.com/benjaminp/six);
  * [python-emoji](https://github.com/carpedm20/emoji).

# Documentation

## Basic usage
  * [List of available bot actions](docs/available-bot-actions.md).
  * [Configuration file documentation](docs/schema-documentation.md).

## Installation
  * [Installing the bot from PyPI](docs/pypi-installation.md).
  * [Installing the bot on Windows](docs/windows-installation.md).
  * [Installing the bot on Fedora](docs/fedora-installation.md).
  * [Installation in Python virtual environment](docs/virtualenv-installation.md).

## Advanced configuration
  * [Controling this bot using systemd](docs/controling-with-systemd.md).
  * [Configuration using environment options](docs/bot-environment-options.md).

## Development
  * [Configuration file schema changes](docs/schema-changes.md).
  * [Building Fedora package](docs/building-fedora-package.md).
