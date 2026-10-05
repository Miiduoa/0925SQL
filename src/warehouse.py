import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_connection(
    schema_path: str | Path | None = None,
    seed_path: str | Path | None = None,
) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    schema = Path(schema_path or ROOT / "sql" / "schema.sql")
    seed = Path(seed_path or ROOT / "sql" / "seed.sql")

    connection.executescript(
        schema.read_text(encoding="utf-8")
    )
    connection.executescript(
        seed.read_text(encoding="utf-8")
    )

    return connection


def integrity_errors(
    connection: sqlite3.Connection,
) -> list[str]:
    errors = []

    integrity = connection.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]
    if integrity != "ok":
        errors.append(
            f"integrity_check: {integrity}"
        )

    foreign_key_rows = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()
    for row in foreign_key_rows:
        errors.append(
            f"foreign_key_check: {tuple(row)}"
        )

    bad_quantity = connection.execute(
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE quantity <= 0
        """
    ).fetchone()[0]
    if bad_quantity:
        errors.append(
            f"non-positive quantities: {bad_quantity}"
        )

    bad_price = connection.execute(
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE unit_price < 0
        """
    ).fetchone()[0]
    if bad_price:
        errors.append(
            f"negative prices: {bad_price}"
        )

    bad_cost = connection.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE unit_cost < 0
        """
    ).fetchone()[0]
    if bad_cost:
        errors.append(
            f"negative costs: {bad_cost}"
        )

    empty_completed = connection.execute(
        """
        SELECT COUNT(*)
        FROM orders AS o
        WHERE o.status = 'completed'
          AND NOT EXISTS (
              SELECT 1
              FROM order_items AS oi
              WHERE oi.order_id = o.order_id
          )
        """
    ).fetchone()[0]
    if empty_completed:
        errors.append(
            f"completed orders without items: {empty_completed}"
        )

    return errors


def run_sql_file(
    connection: sqlite3.Connection,
    path: str | Path,
):
    sql = Path(path).read_text(
        encoding="utf-8"
    )
    return connection.execute(sql).fetchall()
