import os
import subprocess
import webbrowser
from pathlib import Path

def launch_overlay(url: str = "http://localhost:1337"):
    profile_dir = str(Path(__file__).parent / "penguin_profile")

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "chrome",
    ]

    chrome_cmd = None
    for path in chrome_paths:
        if os.path.exists(path.split()[0] if " " in path else path):
            chrome_cmd = path
            break

    if not chrome_cmd:
        webbrowser.open(url)
        return

    args = [
        chrome_cmd,
        f"--app={url}",
        "--window-size=380,460",
        "--window-position=30,30",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-infobars",
        "--disable-extensions",
        "--disable-features=TranslateUI",
        f"--user-data-dir={profile_dir}",
        "--class=penguin-external"
    ]

    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # fallback to webbrowser if launching fails
        webbrowser.open(url)
