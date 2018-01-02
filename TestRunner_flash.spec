# -*- mode: python -*-

block_cipher = None


a = Analysis(['TestRunner_flash.py'],
             pathex=['H:\\MyDocuments\\PyCharmProjects\\Automation'],
             binaries=[],
             datas=[('H:\\MyDocuments\\PyCharmProjects\\Automation\\flash_config.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='TestRunner_flash',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='H:\MyDocuments\PyCharmProjects\Automation\exeicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='TestRunner_flash')
