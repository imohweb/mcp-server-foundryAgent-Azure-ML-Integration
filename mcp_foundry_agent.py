import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from foundry_agent.client import run_foundry_agent_demo  # type: ignore[import]


if __name__ == "__main__":
    run_foundry_agent_demo()
