; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=IcepapCMS
AppVerName=IcepapCMS 0.1
AppPublisher=Cells - Alba
AppPublisherURL=http://www.cells.es
AppSupportURL=http://www.cells.es
AppUpdatesURL=http://www.cells.es
DefaultDirName={pf}\IcepapCMS
DefaultGroupName=IcepapCMS
DisableProgramGroupPage=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Z:\IcepapCMS\src\dist\icepapcms.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_bsddb.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_fsBTree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_helper.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_OOBTree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\cPersistence.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\cPickleCache.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\ExtensionClass.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\mingwm10.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\MSVCR71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\python24.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\pywintypes24.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtAssistant.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtCore4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtCore.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtGui4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtGui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtNetwork4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtNetwork.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtOpenGL4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtOpenGL.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtSql4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtSql.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtSvg4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtSvg.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtXml4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\QtXml.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\sip.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\ThreadLock.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\TimeStamp.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\win32api.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\win32event.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\win32evtlog.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\win32file.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\winlock.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\zlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "Z:\IcepapCMS\src\dist\doc\*"; DestDir: "{app}\doc"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Z:\IcepapCMS\src\dist\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\IcepapCMS"; Filename: "{app}\icepapcms.exe"
Name: "{group}\{cm:UninstallProgram,Icepap CMS}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\IcepapCMS"; Filename: "{app}\icepapcms.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\icepapcms.exe"; Description: "{cm:LaunchProgram,IcepapCMS}"; Flags: nowait postinstall skipifsilent
