import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.warehouse import (
    build_connection,
    integrity_errors,
)


connection = build_connection()
errors = integrity_errors(connection)

if errors:
    for error in errors:
        print(f"FAIL {error}")
    raise SystemExit(1)

print("PASS warehouse integrity")
