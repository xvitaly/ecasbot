; SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
;
; SPDX-License-Identifier: GPL-3.0-or-later

#define VERSION GetVersionNumbersString("..\results\dist\ecasbot.exe")
#define BASEDIR "..\results\dist"

#if GetEnv('CI_HASH') == ''
#define _RELEASE 1
#endif

[Setup]
AppId={{67B50FB5-DEAE-4933-A1DE-4946879B879F}
AppName=EC AntiSpam bot
AppVerName=EC AntiSpam bot
AppPublisher=EasyCoding Team
AppPublisherURL=https://www.easycoding.org/
AppVersion={#VERSION}
AppSupportURL=https://github.com/xvitaly/ecasbot/issues
AppUpdatesURL=https://github.com/xvitaly/ecasbot/releases
DefaultDirName={localappdata}\ecasbot
DefaultGroupName=EC AntiSpam bot
AllowNoIcons=yes
LicenseFile=..\..\..\LICENSE
OutputDir=..\results
OutputBaseFilename={#GetEnv('PREFIX')}_setup
SetupIconFile=..\assets\ecasbot.ico
UninstallDisplayIcon={app}\ecasbot.exe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
ShowLanguageDialog=auto
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=6.1sp1
VersionInfoVersion={#VERSION}
VersionInfoDescription=EC AntiSpam bot
VersionInfoCopyright=(c) 2005-2020 EasyCoding Team. All rights reserved.
VersionInfoCompany=EasyCoding Team

[Messages]
BeveledLabel=EasyCoding Team

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl,locale\en\cm.isl"; InfoBeforeFile: "locale\en\readme.rtf"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl,locale\ru\cm.isl"; InfoBeforeFile: "locale\ru\readme.rtf"

[Types]
Name: standard; Description: "{cm:TypeStandardDescription}"
Name: system; Description: "{cm:TypeSystemDescription}"

[Components]
Name: "core"; Description: "{cm:ComponentCoreDescription}"; Types: standard system; Flags: fixed
Name: "apikey"; Description: "{cm:ComponentAPIKeySubDescription}"; Types: standard system; Flags: exclusive
Name: "apikey\sysenv"; Description: "{cm:ComponentAPIKeySysEnvDescription}"; Types: system; Flags: exclusive restart
Name: "apikey\launcher"; Description: "{cm:ComponentAPIKeyLauncherDescription}"; Types: standard; Flags: exclusive

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "autorun"; Description: "{cm:TaskAutorun}"; GroupDescription: "{cm:TaskCategoryAutorun}"; Flags: unchecked

[Files]
Source: "{#BASEDIR}\ecasbot.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: core
Source: "{#BASEDIR}\ecasbot.json"; DestDir: "{userappdata}\ecasbot"; Flags: ignoreversion; Components: core
Source: "{tmp}\launcher.cmd"; DestDir: "{app}"; Flags: external; Components: apikey\launcher

#ifdef _RELEASE
Source: "{#BASEDIR}\ecasbot.exe.sig"; DestDir: "{app}"; Flags: ignoreversion; Components: core
#endif

[Icons]
Name: "{group}\EC AntiSpam bot"; Filename: "{app}\ecasbot.exe"; Components: "apikey\sysenv"
Name: "{group}\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"
Name: "{group}\{cm:ProgramOnTheWeb,EC AntiSpam bot}"; Filename: "https://github.com/xvitaly/ecasbot"; Components: core
Name: "{userdesktop}\EC AntiSpam bot"; Filename: "{app}\ecasbot.exe"; Components: "apikey\sysenv"; Tasks: desktopicon
Name: "{userdesktop}\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Windows\Start Menu\Programs\Startup\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"; Tasks: autorun

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "APIKEY"; ValueData: "{code:GetAPIKey}"; Flags: uninsdeletevalue; Components: "apikey\sysenv"
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ecasbot"; ValueData: "{app}\ecasbot.exe"; Flags: uninsdeletevalue; Components: "apikey\sysenv"; Tasks: autorun

[Code]
var
    APIKeyPage: TInputQueryWizardPage;

procedure AddAPIKeyPage();
begin
    APIKeyPage := CreateInputQueryPage(wpSelectTasks, CustomMessage('APIKeyPageCaption'), CustomMessage('APIKeyPageDescription'), CustomMessage('APIKeyPageAdditionalText'));
    APIKeyPage.Add(CustomMessage('APIKeyPageInputFieldText'), False)
end;

procedure InitializeWizard();
begin
    AddAPIKeyPage()
end;

function GetAPIKeyInternal(): String;
begin
    Result := APIKeyPage.Values[0]
end;

function GetAPIKey(Value: String): String;
begin
    Result := GetAPIKeyInternal()
end;

function GenerateBotLauncher(FileName: String): Boolean;
var
    Contents: TArrayOfString;
begin
    SetArrayLength(Contents, 6);
    Contents[0] := '@echo off';
    Contents[1] := '';
    Contents[2] := 'title EC AntiSpam bot';
    Contents[3] := 'set APIKEY=' + GetAPIKeyInternal();
    Contents[4] := '';
    Contents[5] := '.\ecasbot.exe';
    Result := SaveStringsToFile(FileName, Contents, False)
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
    if CurPageID = APIKeyPage.ID then
        begin
            if Length(APIKeyPage.Values[0]) < 10 then
                begin
                    MsgBox(CustomMessage('APIKeyPageErrorMessage'), mbError, MB_OK);
                    Result := False
                end
            else
                begin
                    Result := GenerateBotLauncher(ExpandConstant('{tmp}\launcher.cmd'));
                end
        end
    else
        begin
            Result := True
        end
end;
