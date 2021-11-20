# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None


a = Analysis(
    ['src/xFont.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['cairo'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

def get_all_images():
    dir = os.getcwd()
    dir = os.path.join(dir, "src")
    dir = os.path.join(dir, 'icons')
    relate_path = os.path.join("src", "icons")
    ret = []
    for file in os.listdir(dir):
        if file.endswith(".png"):
            ret.append((file, os.path.join(relate_path, file)))
    return ret

images = get_all_images()
for image, path in images:
    a.datas += [ (image, path, 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='xFont',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='xFont',
)
app = BUNDLE(
    coll,
    name='xFont.app',
    icon=None,
    bundle_identifier=None,
)
