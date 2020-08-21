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

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ecasbot',
    version='1.5.1',
    packages=find_packages(),
    package_dir={
        'ecasbot': 'ecasbot',
    },
    url='https://github.com/xvitaly/ecasbot',
    entry_points={
        'console_scripts': [
            'ecasbot = ecasbot.scripts.runbot:main',
        ],
    },
    license='GPLv3',
    install_requires=['pytelegrambotapi', 'requests', 'six', 'emoji'],
    author='Vitaly Zaitsev',
    author_email='vitaly@easycoding.org',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='EC AntiSpam bot for the Telegram messenger',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
