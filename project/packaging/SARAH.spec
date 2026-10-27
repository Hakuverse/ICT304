from pathlib import Path
import sys
from PyInstaller.utils.hooks import collect_data_files, copy_metadata, collect_submodules

root = Path(SPECPATH).parents[1]
datas = collect_data_files('streamlit') + copy_metadata('streamlit', recursive=True)
datas += collect_data_files('altair') + collect_data_files('pydeck')
for name in ['dashboard.py', 'predict.py', 'data_processing.py', 'recommend.py']:
    datas.append((str(root / 'project/code' / name), 'project/code'))
datas += [(str(root / 'project/models'), 'project/models')]
for name in ['sample_roster.csv', 'study_hours_warning_demo.csv']:
    datas.append((str(root / 'project/data' / name), 'project/data'))
hidden = collect_submodules('sklearn', filter=lambda n: '.tests' not in n)
hidden += collect_submodules('streamlit')
a = Analysis([str(root / 'project/packaging/launcher.py')],
             pathex=[str(root / 'project/packaging')], binaries=[], datas=datas,
             hiddenimports=hidden, excludes=['matplotlib', 'pytest', 'IPython'], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='SARAH',
          debug=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='SARAH')
if sys.platform == 'darwin':
    app = BUNDLE(coll, name='SARAH.app', bundle_identifier='edu.sarah.prototype',
                 info_plist={'NSHighResolutionCapable': True})
