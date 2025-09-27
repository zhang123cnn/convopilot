# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['convopilot/voice_keyboard_app.py'],
    pathex=[],
    binaries=[],
    datas=[('./env/lib/python3.10/site-packages/whisper/assets', 'whisper/assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='voice_keyboard_app',
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
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='voice_keyboard_app.app',
    icon=None,
    bundle_identifier=None,
)
