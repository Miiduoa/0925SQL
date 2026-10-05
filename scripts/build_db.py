import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python scripts/build_db.py <output.db>"
        )

    destination = Path(sys.argv[1])

    if destination.exists():
        destination.unlink()

    connection = sqlite3.connect(destination)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        (ROOT / "sql" / "schema.sql").read_text(
            encoding="utf-8"
        )
    )
    connection.executescript(
        (ROOT / "sql" / "seed.sql").read_text(
            encoding="utf-8"
        )
    )
    connection.commit()

    rows = connection.execute(
        """
        SELECT
            COUNT(*) AS orders
        FROM orders
        """
    ).fetchone()[0]

    connection.close()
    print(
        f"built {destination} with {rows} orders"
    )


if __name__ == "__main__":
    main()
