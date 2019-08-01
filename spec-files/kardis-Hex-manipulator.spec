# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Hex-manipulator.py'],
             pathex=['D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('hex.ico', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\hex.ico', 'DATA'),
          ('clear.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\clear.png', 'DATA'),\
          ('debug.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\debug.png', 'DATA'),\
          ('delSett.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\delSett.png', 'DATA'),\
          ('folder.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\folder.png', 'DATA'),\
          ('load.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\load.png', 'DATA'),\
          ('saveSett.png', 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\saveSett.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Hex-manipulator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon = 'D:\\Python_scripts\\2019-07-26_pyHEX\\HEX-Tool-exe\\hex.ico' )
