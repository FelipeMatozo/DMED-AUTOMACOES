# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],  # Diretório base
    binaries=[],
    datas=[  # Inclua todos os arquivos e diretórios necessários
        ('assets/', 'assets/'),  # Inclui todo o diretório assets
        ('banco/', 'banco/'),
        ('templates/', 'templates/'),
        ('IA/', 'IA/'),
        ('copel_icon.ico', '.')  # Coloca o ícone diretamente na pasta raiz do executável
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    icon='copel_icon.ico',  # Agora o ícone está diretamente na raiz
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Menu'
)
