# -*- mode: python ; coding: utf-8 -*-
# Configuración optimizada para PyInstaller - MultiMinecraft Launcher

block_cipher = None

a = Analysis(
    ['MultiMinecraft.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Resources', 'Resources'),
        ('version_manager.py', '.'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'customtkinter.windows',
        'customtkinter.windows.widgets',
        'customtkinter.windows.ctk_tk',
        'minecraft_launcher_lib',
        'minecraft_launcher_lib.install',
        'minecraft_launcher_lib.command',
        'minecraft_launcher_lib.utils',
        'minecraft_launcher_lib.forge',
        'minecraft_launcher_lib.fabric',
        'requests',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'pygetwindow',
        'version_manager',
        'config',
        'tkinter',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'concurrent.futures',
        'threading',
        'json',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MultiMinecraft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Resources/icon.ico',
)
