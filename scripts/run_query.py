import sqlite3
import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit(
        "usage: python scripts/run_query.py <db> <query.sql>"
    )

database = Path(sys.argv[1])
query_file = Path(sys.argv[2])

connection = sqlite3.connect(database)
connection.row_factory = sqlite3.Row

rows = connection.execute(
    query_file.read_text(encoding="utf-8")
).fetchall()

if rows:
    print("\t".join(rows[0].keys()))
    for row in rows:
        print(
            "\t".join(
                str(row[key])
                for key in row.keys()
            )
        )

connection.close()
