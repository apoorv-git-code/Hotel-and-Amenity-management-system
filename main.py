import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    app_path = Path(__file__).with_name("app.py")
    port = os.environ.get("PORT", "8501")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.address=0.0.0.0",
            f"--server.port={port}",
            "--server.headless=true",
        ],
        check=True,
    )
