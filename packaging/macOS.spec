# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from pathlib import Path

hiddenimports = []
hiddenimports += collect_submodules('metaforge')
hiddenimports += ['flatten_dict', 'h5py', 'PIL', 'PIL.Image']

parent_path = Path('metaforge').parent.parent
version_filepath = parent_path / 'metaforge' / 'VERSION'
version_filepath = version_filepath.absolute()
with open(str(version_filepath)) as version_file:
    version = version_file.read().strip()

block_cipher = None

a = Analysis(['../metaforge/__main__.py'],
             pathex=[],
             binaries=[],
             datas=[('../metaforge/VERSION', '.'), ('../metaforge/', 'metaforge/')],
             hiddenimports=hiddenimports,
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

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='__main__',
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
          icon=['../resources/Images/MetaForge.ico'],
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MetaForge.app',  # Change name to MetaForge
)
app = BUNDLE(coll,
             name='MetaForge.app',
             icon='../resources/Images/MetaForge.ico',
             bundle_identifier=None,
             version=version,
)
