"""Keep a localhost port occupied while testing the packaged SARAH app."""
import socket

with socket.socket() as held:
    try:
        held.bind(("127.0.0.1", 8501))
    except OSError:
        held.bind(("127.0.0.1", 0))
    held.listen(1)
    print(f"Held localhost port: {held.getsockname()[1]}", flush=True)
    print("Keep this window open, launch SARAH, and record its different browser port.")
    input("After quitting SARAH, press Enter here to release the held port: ")
