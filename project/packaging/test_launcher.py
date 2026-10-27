import io
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import launcher


class LauncherTests(unittest.TestCase):
    def test_source_paths_do_not_use_working_directory(self):
        root = launcher.bundle_root()
        self.assertTrue((root / 'project/code/dashboard.py').is_file())
        launcher.validate_resources(root)

    def test_frozen_paths_use_bundle(self):
        with patch.object(sys, 'frozen', True, create=True), patch.object(sys, '_MEIPASS', '/bundle space', create=True):
            self.assertEqual(launcher.bundle_root(), Path('/bundle space'))
            self.assertEqual(launcher.child_command(54321, 'abcd'),
                             [sys.executable, '--serve', '54321', '--session', 'abcd'])

    def test_missing_resources_fail_before_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, 'complete application'):
                launcher.validate_resources(Path(directory))

    def test_lock_blocks_second_copy_and_releases(self):
        with tempfile.TemporaryDirectory() as directory:
            a = launcher.InstanceLock(Path(directory) / 'lock')
            b = launcher.InstanceLock(Path(directory) / 'lock')
            try:
                self.assertTrue(a.acquire())
                self.assertFalse(b.acquire())
                a.close()
                self.assertTrue(b.acquire())
            finally:
                a.close()
                b.close()

    def test_port_selection_avoids_occupied_port(self):
        with socket.socket() as occupied:
            occupied.bind(('127.0.0.1', 0))
            self.assertNotEqual(launcher.available_port(), occupied.getsockname()[1])

    def test_health_checks_session_path_and_response(self):
        response = Mock(status=200)
        response.read.return_value = b'ok'
        opener = Mock()
        opener.open.return_value.__enter__ = Mock(return_value=response)
        opener.open.return_value.__exit__ = Mock(return_value=False)
        with patch('launcher.urllib.request.build_opener', return_value=opener):
            self.assertTrue(launcher.is_ready('http://127.0.0.1:1234/abcd'))
            opener.open.assert_called_with('http://127.0.0.1:1234/abcd/_stcore/health', timeout=.25)
            response.read.return_value = b'wrong service'
            self.assertFalse(launcher.is_ready('http://127.0.0.1:1234/abcd'))

    def test_health_failure_is_not_ready(self):
        with patch('launcher.urllib.request.build_opener') as build:
            build.return_value.open.side_effect = OSError('not ready')
            self.assertFalse(launcher.is_ready('http://127.0.0.1:1234/abcd'))

    def test_child_launch_hides_output_and_keeps_parent_pipe(self):
        with tempfile.TemporaryDirectory() as directory, patch('launcher.subprocess.Popen') as start:
            service = launcher.DashboardService(directory)
            service.start()
            options = start.call_args.kwargs
            self.assertEqual(options['stdin'], subprocess.PIPE)
            self.assertEqual(options['stdout'], subprocess.DEVNULL)
            self.assertEqual(options['stderr'], subprocess.DEVNULL)
            self.assertEqual(options['cwd'], Path(directory))
            self.assertTrue(service.url.startswith('http://127.0.0.1:'))
            self.assertNotIn('PYTHONPATH', options['env'])
            self.assertIn('starting', (Path(directory) / 'launcher.log').read_text())

    def test_start_failure_propagates_for_user_message(self):
        with tempfile.TemporaryDirectory() as directory, patch('launcher.subprocess.Popen', side_effect=OSError('denied')):
            with self.assertRaises(OSError):
                launcher.DashboardService(directory).start()

    def test_status_checks_process_before_health(self):
        service = launcher.DashboardService('.')
        service.process = Mock()
        service.process.poll.return_value = 1
        with patch('launcher.is_ready') as health:
            self.assertEqual(service.status(), 'failed')
            health.assert_not_called()

    def test_timeout_and_readiness(self):
        service = launcher.DashboardService('.')
        service.process = Mock()
        service.process.poll.return_value = None
        service.started = 0
        with patch('launcher.time.monotonic', return_value=91), patch('launcher.is_ready', return_value=False):
            self.assertEqual(service.status(), 'timeout')
        with patch('launcher.is_ready', return_value=True):
            self.assertEqual(service.status(), 'ready')

    def test_stop_only_targets_owned_process(self):
        process = Mock()
        process.poll.return_value = None
        process.wait.side_effect = [subprocess.TimeoutExpired('test', 5), 0]
        launcher.stop_process(process)
        process.stdin.close.assert_called_once()
        process.terminate.assert_called_once()
        process.kill.assert_called_once()

    def test_parent_pipe_eof_triggers_exit(self):
        with patch('launcher.os._exit') as exit_process:
            launcher.watch_launcher(io.BytesIO(b''))
            exit_process.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
