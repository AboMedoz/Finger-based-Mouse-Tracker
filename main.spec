# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('mediapipe_modules/hand_landmark/hand_landmark_tracking_cpu.binarypb', 'mediapipe/modules/hand_landmark'),
    ('mediapipe_modules/hand_landmark/hand_landmark_full.tflite', 'mediapipe/modules/hand_landmark'),
    ('mediapipe_modules/palm_detection/palm_detection_full.tflite', 'mediapipe/modules/palm_detection'),
    ('mediapipe_modules/hand_landmark/handedness.txt', 'mediapipe/modules/hand_landmark'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
