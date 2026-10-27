"""Start the local SARAH dashboard from source or a PyInstaller bundle."""
import argparse
from datetime import datetime, timezone
import multiprocessing
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser


def bundle_root():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def state_directory():
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    path = base / "SARAH"
    path.mkdir(parents=True, exist_ok=True)
    return path


class InstanceLock:
    """An OS-held lock: crashes release it without deleting another app's lock."""
    def __init__(self, path):
        self.path = Path(path)
        self.file = None

    def acquire(self):
        handle = self.path.open("a+b")
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if sys.platform == "win32":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            handle.close()
            return False
        self.file = handle
        return True

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None


def validate_resources(root):
    needed = [root / "project/code" / name for name in
              ("dashboard.py", "predict.py", "data_processing.py", "recommend.py")]
    needed += [root / "project/models" / name for name in
               ("early_warning_model.joblib", "confirmatory_g1_model.joblib",
                "confirmatory_g1_g2_model.joblib")]
    if any(not p.is_file() for p in needed):
        raise RuntimeError("SARAH files are missing. Download and extract the complete application again.")


def available_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def child_command(port, token):
    command = [sys.executable]
    if not getattr(sys, "frozen", False):
        command.append(str(Path(__file__).resolve()))
    return command + ["--serve", str(port), "--session", token]


def is_ready(url):
    # Ignore system HTTP proxies for this local-only connection.
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url + "/_stcore/health", timeout=0.25) as response:
            return response.status == 200 and response.read(16) == b"ok"
    except (OSError, ValueError):
        return False


def stop_process(process):
    if process is None:
        return
    if process.stdin:
        process.stdin.close()
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


class DashboardService:
    def __init__(self, state_dir):
        self.state_dir = Path(state_dir)
        self.process = None
        self.url = None
        self.started = None

    def record(self, event):
        # Only fixed lifecycle messages, never app output, inputs, exceptions or CSV data.
        with (self.state_dir / "launcher.log").open("a", encoding="utf-8") as log:
            log.write(f"{datetime.now(timezone.utc).isoformat()} {event}\n")

    def start(self):
        root = bundle_root()
        validate_resources(root)
        port = available_port()
        token = secrets.token_hex(16)
        self.url = f"http://127.0.0.1:{port}/{token}"
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        # Keep config/secrets outside the source checkout. Do not inherit Python paths.
        env = os.environ.copy()
        for key in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
            env.pop(key, None)
        self.process = subprocess.Popen(
            child_command(port, token), cwd=self.state_dir, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=flags,
        )
        self.started = time.monotonic()
        self.record("starting")

    def status(self):
        if self.process is None or self.process.poll() is not None:
            return "failed"
        if is_ready(self.url):
            return "ready"
        if time.monotonic() - self.started >= 90:
            return "timeout"
        return "starting"

    def stop(self):
        stop_process(self.process)
        self.process = None


def watch_launcher(pipe):
    # Parent owns the write end. EOF also occurs if it crashes or is forcibly closed.
    try:
        while pipe.read(1):
            pass
    finally:
        os._exit(0)


def serve(port, token):
    if not token or any(c not in "0123456789abcdef" for c in token):
        raise ValueError("Invalid session path")
    # A windowed Windows EXE has no sys.stdin; the redirected OS fd is still present.
    parent_pipe = os.fdopen(os.dup(0), "rb", buffering=0)
    threading.Thread(target=watch_launcher, args=(parent_pipe,), daemon=True).start()
    root = bundle_root()
    validate_resources(root)
    sys.path.insert(0, str(root / "project/code"))
    from streamlit.web import cli
    sys.argv = ["streamlit", "run", str(root / "project/code/dashboard.py"),
                "--global.developmentMode=false", "--server.address=127.0.0.1",
                f"--server.port={port}", f"--server.baseUrlPath={token}",
                "--browser.serverAddress=127.0.0.1", "--server.headless=true",
                "--browser.gatherUsageStats=false", "--server.fileWatcherType=none"]
    cli.main()


def launch():
    import tkinter as tk
    from tkinter import messagebox, ttk
    root = tk.Tk()
    root.withdraw()
    try:
        directory = state_directory()
        lock = InstanceLock(directory / "launcher.lock")
        if not lock.acquire():
            messagebox.showinfo("SARAH is already open",
                                "Use Open dashboard in the existing SARAH window.\n"
                                "Quit that window before starting another copy.", parent=root)
            root.destroy()
            return
    except OSError:
        messagebox.showerror("SARAH cannot start", "Cannot create SARAH's local settings folder.\n"
                             "Check your user account's folder permissions.", parent=root)
        root.destroy()
        return
    service = DashboardService(directory)
    root.title("SARAH")
    root.geometry("520x270")
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="SARAH", font=("TkDefaultFont", 20, "bold")).pack(anchor="w")
    status = tk.StringVar(value="Starting your local dashboard...")
    ttk.Label(frame, textvariable=status, wraplength=465).pack(anchor="w", pady=12)
    ttk.Label(frame, text="Keep this window open while using SARAH.\n"
              "Closing a browser tab does not stop SARAH.\nUse Quit SARAH when finished.").pack(anchor="w")
    controls = ttk.Frame(frame)
    controls.pack(anchor="w", pady=15)
    def open_dashboard():
        try:
            opened = webbrowser.open(service.url + "/")
        except Exception:
            opened = False
        if not opened:
            status.set("Ready, but the browser did not open. Open this address:\n" + service.url + "/")
    open_button = ttk.Button(controls, text="Open dashboard", state="disabled", command=open_dashboard)
    open_button.pack(side="left", padx=(0, 12))
    def quit_app():
        root.destroy()
    ttk.Button(controls, text="Quit SARAH", command=quit_app).pack(side="left")
    root.protocol("WM_DELETE_WINDOW", quit_app)
    was_ready = False
    def poll():
        nonlocal was_ready
        current = service.status()
        if current in ("failed", "timeout"):
            service.stop()
            service.record(current)
            open_button.configure(state="disabled")
            status.set("SARAH stopped unexpectedly." if was_ready else "SARAH could not finish starting.")
            status.set(status.get() + " Quit and try again.\nIf it continues, report your app version and OS.\n"
                       "Basic startup record: " + str(directory / "launcher.log"))
            return
        if current == "ready" and not was_ready:
            was_ready = True
            service.record("ready")
            status.set("Ready. Your dashboard is available in the browser.")
            open_button.configure(state="normal")
            open_dashboard()
        elif not was_ready and time.monotonic() - service.started > 30:
            status.set("Starting is taking longer than the 30-second target. Please wait...")
        root.after(500, poll)
    root.deiconify()
    try:
        try:
            service.start()
        except (OSError, RuntimeError):
            service.stop()
            status.set("SARAH could not start. Check that the complete application was extracted\n"
                       "and your user folder is writable. Quit and try again.")
        else:
            root.after(500, poll)
        root.mainloop()
    finally:
        service.stop()
        lock.close()


def main():
    multiprocessing.freeze_support()
    for name in ("stdout", "stderr"):
        if getattr(sys, name) is None:
            setattr(sys, name, open(os.devnull, "w"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", type=int)
    parser.add_argument("--session")
    parser.add_argument("--self-test")
    args = parser.parse_args()
    if args.serve is not None:
        serve(args.serve, args.session)
    elif args.self_test:
        from bundle_check import self_test
        self_test(Path(args.self_test), bundle_root())
    else:
        launch()


if __name__ == "__main__":
    main()
