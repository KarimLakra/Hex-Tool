# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Hex-manipulator.py'],
             pathex=['C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool'],
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
a.datas += [('hex.ico', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\hex.ico', 'DATA'),
          ('clear.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\clear.png', 'DATA'),\
          ('debug.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\debug.png', 'DATA'),\
          ('delSett.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\delSett.png', 'DATA'),\
          ('folder.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\folder.png', 'DATA'),\
          ('load.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\load.png', 'DATA'),\
          ('saveSett.png', 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\saveSett.png', 'DATA')]
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
          icon = 'C://Users//Ideapad//AppData//Local//Packages//CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc//LocalState//rootfs//home//kardes//ciptec-Git-projects//Hex-Tool\\hex.ico' )
