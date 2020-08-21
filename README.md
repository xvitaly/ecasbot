# EC AntiSpam bot

[![GitHub version](https://img.shields.io/github/v/release/xvitaly/ecasbot?sort=semver&color=brightgreen&logo=git&logoColor=white)](https://github.com/xvitaly/ecasbot/releases)
[![GitHub CI status](https://github.com/xvitaly/ecasbot/workflows/Python%20CI/badge.svg?branch=dev)](https://github.com/xvitaly/ecasbot/actions)
[![Build status](https://travis-ci.org/xvitaly/ecasbot.svg?branch=master)](https://travis-ci.org/xvitaly/ecasbot)
[![LGTM grade](https://img.shields.io/lgtm/grade/python/g/xvitaly/ecasbot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xvitaly/ecasbot/context:python)
[![LGTM alerts](https://img.shields.io/lgtm/alerts/g/xvitaly/ecasbot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/xvitaly/ecasbot/alerts/)
[![CodeFactor](https://www.codefactor.io/repository/github/xvitaly/ecasbot/badge/dev)](https://www.codefactor.io/repository/github/xvitaly/ecasbot/overview/dev)
[![GitHub issues](https://img.shields.io/github/issues/xvitaly/ecasbot.svg?label=issues)](https://github.com/xvitaly/ecasbot/issues)
---

EC AntiSpam bot for the [Telegram](https://telegram.org/) messenger will automatically detect and block multimedia messages, links from the newly joined users, some common spam bots and users who added them to super-groups.

Warning! Do not use `dev` branch in production due to lots of breaking changes. Use `master` or `stable` instead.

# License
GNU General Public License version 3. You can find it here: [LICENSE](LICENSE). External libraries can use another licenses, compatible with GNU GPLv3.

# Requirements
 * Python 3.6+;
 * [python-pytelegrambotapi](https://github.com/eternnoir/pyTelegramBotAPI);
 * [python-requests](https://github.com/requests/requests);
 * [python-six](https://github.com/benjaminp/six);
 * [python-emoji](https://github.com/carpedm20/emoji).

# Documentation
 * [List of available bot actions](docs/available-bot-actions.md).
 * [Installation in Python virtual environment](docs/virtualenv-installation.md).
 * [Controling this bot using systemd](docs/controling-with-systemd.md).
 * [Configuration file documentation](docs/schema-documentation.md).
 * [Configuration using environment options](docs/bot-environment-options.md).
 * [Building Fedora package](docs/building-fedora-package.md).
