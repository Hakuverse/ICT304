"""Run developer checks; not a replacement for GUI or clean-device testing."""
import argparse
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

from launcher import available_port, is_ready, stop_process


def check(command, output):
    env = os.environ.copy()
    for key in ('PYTHONHOME', 'PYTHONPATH', 'VIRTUAL_ENV'):
        env.pop(key, None)
    env['PATH'] = str(Path(os.environ.get('SystemRoot', '/usr')) / ('System32' if os.name == 'nt' else 'bin'))
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    with tempfile.TemporaryDirectory(prefix='SARAH external folder ') as directory:
        smoke = Path(directory) / 'smoke.json'
        subprocess.run(command + ['--self-test', str(smoke)], cwd=directory, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=flags, check=True, timeout=120)
        results = json.loads(smoke.read_text(encoding='utf-8'))
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for end in ('normal_stop', 'parent_pipe_closed'):
            port, token = available_port(), secrets.token_hex(16)
            url = f'http://127.0.0.1:{port}/{token}'
            process = subprocess.Popen(command + ['--serve', str(port), '--session', token],
                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                cwd=directory, env=env, creationflags=flags)
            started = time.monotonic()
            try:
                while not is_ready(url):
                    if process.poll() is not None:
                        raise RuntimeError(f'Server exited: {process.returncode}')
                    if time.monotonic() - started > 90:
                        raise TimeoutError('Server did not become ready')
                    time.sleep(.2)
                health_time = round(time.monotonic() - started, 3)
                with opener.open(url + '/', timeout=5) as response:
                    html = response.read().decode()
                assert '<div id="root">' in html
                assets = re.findall(r'(?:src|href)="(\./static/[^\"]+)"', html)
                assert assets
                for asset in assets:
                    with opener.open(url + '/' + asset.removeprefix('./'), timeout=5) as response:
                        assert response.status == 200 and response.read(1)
                if end == 'normal_stop':
                    stop_process(process)
                else:
                    process.stdin.close()
                    process.wait(timeout=10)
                # Windows venv Python may have a redirector process. Allow its
                # interpreter child to observe pipe EOF and release the socket.
                deadline = time.monotonic() + 10
                while True:
                    with socket.socket() as sock:
                        if sock.connect_ex(('127.0.0.1', port)) != 0:
                            break
                    if time.monotonic() >= deadline:
                        raise AssertionError('Server port still open after shutdown')
                    time.sleep(.1)
                results[end] = {'health_seconds_not_GUI_startup': health_time, 'static_assets': len(assets),
                                'shutdown': 'passed'}
            finally:
                stop_process(process)
        results['scope'] = 'Developer smoke check; no clean-device, GUI timing, downloaded trust or macOS claim.'
        output.write_text(json.dumps(results, indent=2), encoding='utf-8')
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    command = ([str(args.executable.resolve())] if args.executable else
               [sys.executable, str(Path(__file__).with_name('launcher.py').resolve())])
    check(command, args.output.resolve())
