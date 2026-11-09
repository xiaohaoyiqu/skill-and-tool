"""Launch the source checkout from any working directory, without shell wrappers."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sklib.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
