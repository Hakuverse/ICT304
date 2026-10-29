"""Build a versioned test package on its native Windows/macOS platform."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import distributions
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def run(args, **kwargs):
    subprocess.run([str(a) for a in args], check=True, **kwargs)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def platform_tag(system=None, machine=None):
    system = system or platform.system()
    machine = (machine or platform.machine()).lower()
    if system == 'Windows' and machine in ('amd64', 'x86_64'):
        return 'windows-x64'
    if system == 'Darwin' and machine == 'arm64':
        return 'macos-arm64'
    raise ValueError('Build on Windows x64 or native Apple Silicon macOS. Other targets are not agreed.')


def valid_version(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,49}', value):
        raise ValueError('Use a short version containing only letters, digits, dots and hyphens.')
    return value


def source_commit():
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'],
                                     cwd=ROOT, text=True)
    if status.strip():
        raise RuntimeError('Commit or set aside local changes before building a versioned package.')
    return commit


def copy_notices(target, bundle):
    """Keep the available dependency notices plus Python/Tk runtime notices."""
    target.mkdir(parents=True)
    inventory = []
    for dist in distributions():
        name = re.sub(r'[^A-Za-z0-9_.-]', '_', dist.metadata.get('Name', 'unknown'))
        inventory.append(f'{name}=={dist.version}')
        package_dir = target / name
        package_dir.mkdir(exist_ok=True)
        # Metadata includes project URLs/license expressions when no license file is shipped.
        metadata = dist.read_text('METADATA')
        if metadata:
            (package_dir / 'METADATA.txt').write_text(metadata, encoding='utf-8')
        for file in dist.files or []:
            if any(word in str(file).lower() for word in ('license', 'licence', 'copying', 'notice')):
                source = Path(dist.locate_file(file))
                if source.is_file():
                    # Flatten metadata paths; never allow an upstream path to escape target.
                    filename = hashlib.sha256(str(file).encode()).hexdigest()[:12] + '-' + source.name
                    shutil.copyfile(source, package_dir / filename)
    python_notices = target / 'python-runtime'
    python_notices.mkdir()
    candidates = [Path(sys.base_prefix) / 'LICENSE.txt', Path(sys.base_prefix) / 'LICENSE',
                  Path(sys.base_prefix) / 'Resources/English.lproj/License.rtf']
    for candidate in candidates:
        if candidate.is_file():
            shutil.copyfile(candidate, python_notices / candidate.name)
    for source in bundle.rglob('*'):
        if source.is_file() and any(word in source.name.lower() for word in ('license', 'licence', 'copying', 'notice')):
            relative = source.relative_to(bundle)
            dest = target / 'bundled-runtime' / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
    (target / 'packages.txt').write_text('\n'.join(sorted(inventory)) + '\n', encoding='utf-8')
    (target / 'README.txt').write_text(
        'Dependency metadata and available licence notices from this build environment are included.\n'
        'The environment inventory can include build/test tools not shipped in the executable.\n'
        'Keep these notices with the package. Review the inventory and bundled runtime notices\n'
        'before the final public release under issue #118.\n', encoding='utf-8')


def start_guide(tag):
    opening = ('Keep this whole folder together, including _internal. Double-click SARAH.exe.'
               if tag == 'windows-x64' else
               'Extract the ZIP using Archive Utility. Open SARAH.app from Finder.\n'
               'You can copy SARAH.app into Applications; keep this package for samples and notices.')
    return f'''SARAH - unsigned prototype test package

1. {opening}
2. Wait for the launcher to say Ready and open your default browser.
3. Use the form for one student, or upload a fictional sample CSV for a class.
4. Downloads go to the browser's normal download location.
5. Click Quit SARAH in the small launcher window when finished.
   Closing a browser tab alone does not stop SARAH.

No Python installation or terminal commands are needed for normal use.
The service runs on your computer. Core predictions work without internet.
Do not run the Windows executable directly inside an unextracted ZIP.

This package is not signed by a verified publisher or notarized by Apple.
Your computer may warn or block it. Record the exact message and contact the
team. Do not disable security protections. A blocked launch is not a passed check.

Use fictional students for testing. Predictions are estimates for human review,
not decisions about a student. Study hours above 12 receive a warning; the
accepted range is 0-40 and values at or below 12 are not guaranteed reliable.

Examples: sample_roster.csv has two valid and two invalid rows in Confirmatory
mode. study_hours_warning_demo.csv has two valid rows, one with 40 study hours.
Leave G2 blank for G1-only predictions; zero is a supplied grade.

build-info.json identifies the source commit and build environment.
This package needs the checks in issues #114-#117 before release under #118.
'''


def archive_package(folder, archive, tag):
    if tag == 'macos-arm64':
        # Preserve .app symlinks and executable modes; ordinary zipfile writing does not.
        run(['/usr/bin/ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', folder, archive])
    else:
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zipped:
            for file in sorted(folder.rglob('*')):
                if file.is_file():
                    zipped.write(file, file.relative_to(folder.parent))


def build(version):
    version = valid_version(version)
    tag = platform_tag()
    commit = source_commit()
    name = f'SARAH-{version}-{tag}-{commit[:7]}'
    output = ROOT / 'dist/packages'
    output.mkdir(parents=True, exist_ok=True)
    archive = output / (name + '.zip')
    if archive.exists():
        raise FileExistsError('Package already exists. Keep it as evidence or choose a new version.')
    # Import check catches missing Tk before an expensive build, without requiring a display.
    import tkinter
    tkinter.Tcl()
    run([sys.executable, '-m', 'pip', 'check'])
    with tempfile.TemporaryDirectory(prefix='SARAH package build ') as temp:
        temp = Path(temp)
        dist = temp / 'built'
        run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
             '--distpath', dist, '--workpath', temp / 'work', ROOT / 'project/packaging/SARAH.spec'], cwd=ROOT)
        folder = temp / name
        if tag == 'windows-x64':
            shutil.copytree(dist / 'SARAH', folder)
            executable = folder / 'SARAH.exe'
            bundle = folder / '_internal'
        else:
            folder.mkdir()
            shutil.copytree(dist / 'SARAH.app', folder / 'SARAH.app', symlinks=True)
            executable = folder / 'SARAH.app/Contents/MacOS/SARAH'
            bundle = folder / 'SARAH.app/Contents/Resources'
        (folder / 'START-HERE.txt').write_text(start_guide(tag), encoding='utf-8')
        for sample in ('sample_roster.csv', 'study_hours_warning_demo.csv'):
            shutil.copyfile(ROOT / 'project/data' / sample, folder / sample)
        copy_notices(folder / 'third-party-notices', bundle)
        freeze = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
        (folder / 'build-environment.txt').write_text(freeze, encoding='utf-8')
        info = {
            'version': version, 'source_commit': commit, 'platform': tag,
            'built_utc': datetime.now(timezone.utc).isoformat(),
            'build_os': platform.platform(), 'python': platform.python_version(),
            'signing': 'No publisher signing or Apple notarization; Mac tool ad-hoc signing only if applied.',
            'status': 'test candidate; manual platform/security/startup checks pending',
            'executable_sha256': sha256(executable),
            'models_sha256': {p.name: sha256(p) for p in (ROOT / 'project/models').glob('*.joblib')},
        }
        (folder / 'build-info.json').write_text(json.dumps(info, indent=2), encoding='utf-8')
        run([sys.executable, ROOT / 'project/packaging/check_runtime.py', '--executable', executable,
             '--output', folder / 'runtime-check.json'])
        archive_package(folder, archive, tag)
        try:
            # Verify the actual archive, not just the folder used to create it.
            extracted = temp / 'extracted package with spaces'
            extracted.mkdir()
            if tag == 'macos-arm64':
                run(['/usr/bin/ditto', '-x', '-k', archive, extracted])
                actual_exe = extracted / name / 'SARAH.app/Contents/MacOS/SARAH'
            else:
                with zipfile.ZipFile(archive) as zipped:
                    zipped.extractall(extracted)
                actual_exe = extracted / name / 'SARAH.exe'
            run([sys.executable, ROOT / 'project/packaging/check_runtime.py', '--executable', actual_exe,
                 '--output', output / (name + '-extracted-check.json')])
        except Exception:
            # Preserve failure evidence but ensure this is not presented as a ready candidate.
            archive.rename(archive.with_suffix('.failed.zip'))
            raise
        (output / (name + '.sha256')).write_text(f'{sha256(archive)}  {archive.name}\n', encoding='utf-8')
        (output / (name + '-build-info.json')).write_text(json.dumps(info, indent=2), encoding='utf-8')
        print(f'Test candidate ready: {archive}\nSHA-256: {sha256(archive)}\nBytes: {archive.stat().st_size}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    build(args.version)
