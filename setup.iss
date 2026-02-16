; Script de Inno Setup para MultiMinecraft Launcher
; Genera un instalador profesional tipo .exe

#define MyAppName "MultiMinecraft Launcher"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "Monkey Studio"
#define MyAppURL "https://github.com/yourusername/MultiMinecraft"
#define MyAppExeName "MultiMinecraft.exe"
#define MyAppId "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

[Setup]
; Información básica de la aplicación
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=MultiMinecraft_Installer
SetupIconFile=Resources\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

; Información de desinstalación
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Archivo ejecutable único (onefile)
Source: "dist\MultiMinecraft.exe"; DestDir: "{app}"; Flags: ignoreversion
; Si usas modo onedir (carpeta), descomenta la línea siguiente y comenta la anterior:
; Source: "dist\MultiMinecraft\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Ejecutar el launcher después de la instalación (opcional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Función para verificar si Java está instalado
function IsJavaInstalled(): Boolean;
var
  JavaVersion: String;
begin
  Result := RegQueryStringValue(HKLM, 'SOFTWARE\JavaSoft\Java Runtime Environment', 'CurrentVersion', JavaVersion);
  if not Result then
    Result := RegQueryStringValue(HKLM, 'SOFTWARE\JavaSoft\JDK', 'CurrentVersion', JavaVersion);
end;

// Función para verificar requisitos antes de instalar
function InitializeSetup(): Boolean;
var
  JavaMissing: Boolean;
  ErrorCode: Integer;
begin
  Result := True;
  JavaMissing := not IsJavaInstalled;
  
  if JavaMissing then
  begin
    if MsgBox('Java Runtime Environment no está instalado en el sistema.' + #13#10 +
              'Minecraft requiere Java para funcionar.' + #13#10 + #13#10 +
              '¿Deseas abrir la página de descarga de Java ahora?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.java.com/download/', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
    end;
    // Continuar con la instalación de todas formas
  end;
end;

