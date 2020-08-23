@echo off

rem EC AntiSpam bot for the Telegram messenger
rem Copyright (c) 2017 - 2020 EasyCoding Team
rem
rem This program is free software: you can redistribute it and/or modify
rem it under the terms of the GNU General Public License as published by
rem the Free Software Foundation, either version 3 of the License, or
rem (at your option) any later version.
rem
rem This program is distributed in the hope that it will be useful,
rem but WITHOUT ANY WARRANTY; without even the implied warranty of
rem MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
rem GNU General Public License for more details.
rem
rem You should have received a copy of the GNU General Public License
rem along with this program. If not, see <http://www.gnu.org/licenses/>.

title Building release binaries for Windows...

set RELVER=151
set GPGKEY=A989AAAA
set PYTHONOPTIMIZE=1

echo Removing previous build results...
if exist results rd /S /Q results

echo Starting build process using PyInstaller...
pyinstaller ^
    --log-level=INFO ^
    --distpath=results\dist ^
    --workpath=results\build ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --noupx ^
    --name=ecasbot ^
    --version-file=assets\version.txt ^
    --manifest=assets\ecasbot.manifest ^
    --icon=assets\ecasbot.ico ^
    ..\..\ecasbot\scripts\runbot.py

echo Signing binaries...
"%ProgramFiles(x86)%\GnuPG\bin\gpg.exe" --sign --detach-sign --default-key %GPGKEY% results\dist\ecasbot.exe

echo Compiling Installer...
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" inno\ecasbot.iss

echo Signing built artifacts...
"%ProgramFiles(x86)%\GnuPG\bin\gpg.exe" --sign --detach-sign --default-key %GPGKEY% results\ecasbot_%RELVER%.exe

echo Removing temporary files and directories...
del ecasbot.spec
rd /S /Q "results\build"
rd /S /Q "results\dist"
