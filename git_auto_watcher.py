#!/usr/bin/env python3
"""
Automatic GitHub Sync Watcher — Agentic AI Trader
Monitors local files for changes and automatically commits & pushes to GitHub.
"""

import os
import sys
import time
import subprocess

GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"
if not os.path.exists(GIT_PATH):
    GIT_PATH = "git"

WATCH_EXTENSIONS = ('.py', '.html', '.js', '.css', '.json', '.yaml', '.txt', '.md')
CHECK_INTERVAL_SECONDS = 10

def run_git(args):
    try:
        res = subprocess.run([GIT_PATH] + args, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def has_changes():
    stdout, _, _ = run_git(['status', '--porcelain'])
    return len(stdout) > 0

def auto_push():
    print(f"🔄 Changes detected! Committing and pushing to GitHub...")
    run_git(['add', '.'])
    stdout, stderr, code = run_git(['commit', '-m', f'Auto-sync update: {time.strftime("%Y-%m-%d %H:%M:%S")}'])
    stdout, stderr, code = run_git(['push', 'origin', 'main'])
    if code == 0:
        print("✅ Successfully pushed updates to GitHub!")
        print("🚀 Vercel & Render auto-deployments triggered.")
    else:
        print(f"❌ Push error: {stderr}")

def main():
    print("========================================================")
    print("  Automatic GitHub Sync Watcher Started")
    print("========================================================")
    print(f"Monitoring folder for file changes every {CHECK_INTERVAL_SECONDS} seconds...")
    print("Press Ctrl+C to stop.")
    print("--------------------------------------------------------")

    last_sync = 0
    try:
        while True:
            if has_changes():
                now = time.time()
                if now - last_sync > 5:
                    auto_push()
                    last_sync = now
            time.sleep(CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")

if __name__ == '__main__':
    main()
