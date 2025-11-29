import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure src/ is on sys.path so we can import mcp_server package
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from mcp_server.main import run_server  # type: ignore[import]


if __name__ == "__main__":
    run_server()
