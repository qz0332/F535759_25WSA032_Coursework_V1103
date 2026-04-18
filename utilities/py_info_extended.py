#!/usr/bin/env python3
"""
Python environment diagnostics
- Interpreter path & version
- Virtual env / conda detection
- site-packages locations (global & user)
- pip executable and version
- Installed packages (fast summary)
- sys.path
- Encoding & locale
- Platform & architecture
- Key environment variables (PATH/PYTHONPATH)
- VS Code Python hints (if running under VS Code)
"""

import os
import sys
import platform
import locale
import subprocess
import shutil
from datetime import datetime

def header(title: str):
  print("\n" + "=" * 80)
  print(title)
  print("=" * 80)

def safe_run(cmd):
  try:
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, shell=False)
    return out.strip()
  except Exception as e:
    return f"<error: {e}>"

def print_kv(key, value):
  print(f"{key:24} {value}")

def main():
  header("Python Diagnostics")
  print_kv("Timestamp (UTC):", datetime.utcnow().isoformat() + "Z")

  # Interpreter basics
  header("Interpreter")
  print_kv("sys.executable:", sys.executable)
  print_kv("sys.version:", sys.version.replace("\n", " "))
  print_kv("Implementation:", platform.python_implementation())
  print_kv("Version tuple:", ".".join(map(str, sys.version_info[:3])))

  # Environment detection
  header("Environment (venv / conda)")
  venv = os.environ.get("VIRTUAL_ENV")
  conda_prefix = os.environ.get("CONDA_PREFIX")
  conda_default_env = os.environ.get("CONDA_DEFAULT_ENV")
  print_kv("VIRTUAL_ENV:", venv or "<none>")
  print_kv("CONDA_PREFIX:", conda_prefix or "<none>")
  print_kv("CONDA_DEFAULT_ENV:", conda_default_env or "<none>")
  print_kv("Base prefix:", getattr(sys, "base_prefix", "<n/a>"))
  print_kv("Prefix:", sys.prefix)
  print_kv("Is venv (heuristic):", str(getattr(sys, "base_prefix", sys.prefix) != sys.prefix))

  # site-packages locations
  header("Site / User Site")
  try:
    import site
    sp = site.getsitepackages() if hasattr(site, "getsitepackages") else []
    print_kv("site.getsitepackages():", sp or "<n/a>")
    print_kv("site.getusersitepackages():", site.getusersitepackages())
    print_kv("site.getuserbase():", site.getuserbase())
  except Exception as e:
    print_kv("site info:", f"<error: {e}>")

  # pip info
  header("pip")
  pip_path = shutil.which("pip") or "<not in PATH>"
  pip3_path = shutil.which("pip3") or "<not in PATH>"
  print_kv("pip (which):", pip_path)
  print_kv("pip3 (which):", pip3_path)
  # pip used by this interpreter
  pip_for_this = [sys.executable, "-m", "pip", "--version"]
  print_kv("pip (module) --version:", safe_run(pip_for_this))
  # show pip path list (brief)
  print_kv("pip (module) executable:", safe_run([sys.executable, "-m", "pip", "show", "pip"]))
  # installed summary (first 50)
  try:
    out = safe_run([sys.executable, "-m", "pip", "list", "--format=columns"])
    lines = out.splitlines()
    if len(lines) > 1:
      head = lines[:1] + lines[1:51]
      print("\n".join(head))
      if len(lines) > 51:
        print(f"... ({len(lines)-1-50} more)")
    else:
      print(out)
  except Exception as e:
    print_kv("pip list:", f"<error: {e}>")

  # sys.path
  header("sys.path")
  for i, p in enumerate(sys.path):
    print(f"[{i:02d}] {p}")

  # Encoding & locale
  header("Encoding & Locale")
  print_kv("fsencoding:", sys.getfilesystemencoding())
  print_kv("stdout.encoding:", getattr(sys.stdout, "encoding", "<n/a>"))
  print_kv("stderr.encoding:", getattr(sys.stderr, "encoding", "<n/a>"))
  try:
    print_kv("locale.getpreferredencoding():", locale.getpreferredencoding(False))
  except Exception as e:
    print_kv("locale error:", str(e))

  # Platform & architecture
  header("Platform")
  print_kv("platform:", platform.platform())
  print_kv("system:", platform.system())
  print_kv("release:", platform.release())
  print_kv("machine:", platform.machine())
  print_kv("processor:", platform.processor() or "<blank>")
  print_kv("architecture:", " / ".join(platform.architecture()))
  print_kv("Python build:", " ".join(platform.python_build()))
  print_kv("Python compiler:", platform.python_compiler())

  # Key environment variables
  header("Environment Variables")
  for k in ["PATH", "PYTHONPATH", "VIRTUAL_ENV", "CONDA_DEFAULT_ENV", "CONDA_PREFIX"]:
    v = os.environ.get(k)
    if v:
      if k == "PATH":
        # Show PATH components on separate lines (Windows-friendly)
        print("PATH components:")
        for part in v.split(os.pathsep):
          print(f"  - {part}")
      else:
        print_kv(k + ":", v)
    else:
      print_kv(k + ":", "<not set>")

  # VS Code hints
  header("VS Code Hints")
  # These are present when launched from VS Code's Python extension/terminal
  print_kv("VSCODE_PID:", os.environ.get("VSCODE_PID", "<not set>"))
  print_kv("VSCODE_INJECTION:", os.environ.get("VSCODE_INJECTION", "<not set>"))
  print_kv("PYTHONIOENCODING:", os.environ.get("PYTHONIOENCODING", "<not set>"))
  print_kv("PYTHONUNBUFFERED:", os.environ.get("PYTHONUNBUFFERED", "<not set>"))
  # VS Code-selected interpreter (from Python extension), if exposed
  print_kv("VIRTUAL_ENV (again):", os.environ.get("VIRTUAL_ENV", "<not set>"))

  # Import test (optional quick sanity check)
  header("Import Sanity Check (top packages)")
  test_pkgs = ["pip", "setuptools", "wheel"]
  for pkg in test_pkgs:
    try:
      __import__(pkg)
      print_kv(f"import {pkg}:", "OK")
    except Exception as e:
      print_kv(f"import {pkg}:", f"FAIL ({e})")

  print("\nDone.")

if __name__ == "__main__":
  main()