# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/case_file_organizer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/core', 'core'),
        ('src/gui', 'gui'),
        ('src/utils', 'utils'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'core.config_manager',
        'core.pattern_manager',
        'gui.progress_window',
        'utils.logger',
        'utils.file_utils',
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
    name='Case File Organizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
) 