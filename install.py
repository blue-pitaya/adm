import os
import shutil
from pathlib import Path

if __name__ == "__main__":
    script_dir = Path(__file__).parent.resolve()
    source = script_dir / "adm.py"
    if not source.exists():
        raise Exception("Source file not found")
    dest_dir = Path.home() / ".local" / "bin"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "adm"
    shutil.copy2(source, dest)
    print(f"Copied {source} to {dest}")
    os.chmod(dest, 0o755)
    print(f"Made {dest} executable")
