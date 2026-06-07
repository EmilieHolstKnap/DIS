import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from database import init_db

init_db()