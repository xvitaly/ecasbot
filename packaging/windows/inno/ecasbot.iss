; SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
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
ChangesEnvironment=yes
VersionInfoVersion={#VERSION}
VersionInfoDescription=EC AntiSpam bot
VersionInfoCopyright=(c) 2017-2023 EasyCoding Team. All rights reserved.
VersionInfoCompany=EasyCoding Team

[Messages]
BeveledLabel=EasyCoding Team

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl,locale\en\cm.isl"; InfoBeforeFile: "locale\en\readme.rtf"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl,locale\ru\cm.isl"; InfoBeforeFile: "locale\ru\readme.rtf"

[Types]
Name: system; Description: "{cm:TypeSystemDescription}"
Name: standard; Description: "{cm:TypeStandardDescription}"
Name: nokeys; Description: "{cm:TypeNoKeysDescription}"

[Components]
Name: "core"; Description: "{cm:ComponentCoreDescription}"; Types: standard system nokeys; Flags: fixed
Name: "apikey"; Description: "{cm:ComponentAPIKeySubDescription}"; Types: standard system nokeys; Flags: exclusive
Name: "apikey\sysenv"; Description: "{cm:ComponentAPIKeySysEnvDescription}"; Types: system; Flags: exclusive
Name: "apikey\launcher"; Description: "{cm:ComponentAPIKeyLauncherDescription}"; Types: standard; Flags: exclusive
Name: "apikey\nokeys"; Description: "{cm:ComponentAPIKeyNoKeyDescription}"; Types: nokeys; Flags: exclusive

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "autorun"; Description: "{cm:TaskAutorun}"; GroupDescription: "{cm:TaskCategoryAutorun}"; Components: "apikey\sysenv or apikey\launcher"; Flags: unchecked
Name: "addtopath"; Description: "{cm:TaskAddToPath}"; GroupDescription: "{cm:TaskCategoryAddToPath}"; Components: core; Flags: unchecked

[Files]
Source: "{#BASEDIR}\ecasbot.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: core
Source: "{#BASEDIR}\ecasbot.json"; DestDir: "{userappdata}\ecasbot"; Flags: onlyifdoesntexist; Components: core
Source: "{tmp}\launcher.cmd"; DestDir: "{app}"; Flags: external; Components: apikey\launcher

#ifdef _RELEASE
Source: "{#BASEDIR}\ecasbot.exe.sig"; DestDir: "{app}"; Flags: ignoreversion; Components: core
#endif

[Icons]
Name: "{group}\EC AntiSpam bot"; Filename: "{app}\ecasbot.exe"; Components: "apikey\sysenv"
Name: "{group}\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"
Name: "{group}\{cm:ProgramOnTheWeb,EC AntiSpam bot}"; Filename: "https://github.com/xvitaly/ecasbot"; Components: core
Name: "{userdesktop}\EC AntiSpam bot"; Filename: "{app}\ecasbot.exe"; Components: "apikey\sysenv or apikey\nokeys"; Tasks: desktopicon
Name: "{userdesktop}\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Windows\Start Menu\Programs\Startup\EC AntiSpam bot"; Filename: "{app}\launcher.cmd"; IconFilename: "{app}\ecasbot.exe"; Components: "apikey\launcher"; Tasks: autorun

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "APIKEY"; ValueData: "{code:GetAPIKey}"; Flags: uninsdeletevalue; Components: "apikey\sysenv"
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ecasbot"; ValueData: "{app}\ecasbot.exe"; Flags: uninsdeletevalue; Components: "apikey\sysenv"; Tasks: autorun
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{code:PathNewEntry|{app}}"; Tasks: addtopath; Check: PathIsClean(ExpandConstant('{app}'))

[Code]
var
    APIKeyPage: TInputQueryWizardPage;

function IsUpgrade(): Boolean;
begin
    Result := RegKeyExists(HKEY_CURRENT_USER, ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1'))
end;

function GetEnvValue(EnvName: String): String;
var
    EnvValue: String;
begin
    if RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', EnvName, EnvValue) then
        begin
            Result := EnvValue
        end
    else
        begin
            Result := ''
        end
end;

procedure AddAPIKeyPage();
begin
    APIKeyPage := CreateInputQueryPage(wpSelectTasks, CustomMessage('APIKeyPageCaption'), CustomMessage('APIKeyPageDescription'), CustomMessage('APIKeyPageAdditionalText'));
    APIKeyPage.Add(CustomMessage('APIKeyPageInputFieldText'), False)
    if IsUpgrade() and WizardIsComponentSelected('apikey\sysenv') then
        begin
            APIKeyPage.Values[0] := GetEnvValue('APIKEY')
        end
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

function VerifyAPICredentials(): Boolean;
begin
    Result := Length(GetAPIKeyInternal()) < 10
end;

function IsKeylessInstallation(): Boolean;
begin
    Result := WizardIsComponentSelected('apikey\nokeys')
end;

function GenerateLauncher(FileName: String): Boolean;
var
    Contents: TArrayOfString;
begin
    SetArrayLength(Contents, 6);
    Contents[0] := '@echo off';
    Contents[1] := '';
    Contents[2] := 'title EC AntiSpam bot';
    Contents[3] := 'set APIKEY=' + GetAPIKeyInternal();
    Contents[4] := '';
    Contents[5] := '.\ecasbot.exe %*';
    Result := SaveStringsToFile(FileName, Contents, False)
end;

function PathIsClean(InstallPath: String): Boolean;
var
    CurrentPath: String;
begin
    if RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath) then
        begin
            Result := Pos(InstallPath, CurrentPath) = 0
        end
    else
        begin
            Result := True
        end
end;

function PathNewEntry(InstallPath: String): String;
var
    CurrentPath: String;
begin
    if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath) then
        begin
            CurrentPath := ''
        end;
    if Length(CurrentPath) > 0 then
        begin
            if CompareStr(Copy(CurrentPath, Length(CurrentPath), 1), ';') = 0 then
                begin
                    Result := CurrentPath + InstallPath + ';'
                end
            else
                begin
                    Result := CurrentPath + ';' + InstallPath + ';'
                end
        end
    else
        begin
            Result := InstallPath + ';'
        end
end;

procedure PathRemoveEntry(InstallPath: String);
var
    CurrentPath: String;
    Position: Integer;
    LI, RI: Integer;
begin
    if RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath) then
        begin
            Position := Pos(InstallPath, CurrentPath);
            if Position > 0 then
                begin
                    if CompareStr(Copy(CurrentPath, Position, 1), ';') = 0 then LI := 1 else LI := 0;
                    if (CompareStr(Copy(CurrentPath, Length(CurrentPath), 1), ';') = 0) and (LI = 1) then RI := 0 else RI := 1;
                    Delete(CurrentPath, Position - LI, Length(CurrentPath) + RI);
                    RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', CurrentPath)
                end
        end
end;

function ShouldSkipPage(CurPageID: Integer): Boolean;
begin
    if CurPageID = APIKeyPage.ID then
        begin
            Result := IsKeylessInstallation()
        end
    else
        begin
            Result := False
        end
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
    if CurPageID = APIKeyPage.ID then
        begin
            if (VerifyAPICredentials()) then
                begin
                    MsgBox(CustomMessage('APIKeyPageErrorMessage'), mbError, MB_OK);
                    Result := False
                end
            else
                begin
                    Result := GenerateLauncher(ExpandConstant('{tmp}\launcher.cmd'));
                end
        end
    else
        begin
            Result := True
        end
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
    if CurUninstallStep = usPostUninstall then
        begin
            PathRemoveEntry(ExpandConstant('{app}'))
        end
end;
