import sqlite3
import unittest
from pathlib import Path

from src.warehouse import (
    ROOT,
    build_connection,
    integrity_errors,
    run_sql_file,
)


class SqlMartTests(unittest.TestCase):
    def setUp(self):
        self.connection = build_connection()

    def tearDown(self):
        self.connection.close()

    def test_integrity_checks_pass(self):
        self.assertEqual(
            integrity_errors(self.connection),
            [],
        )

    def test_completed_revenue_is_known(self):
        revenue = self.connection.execute(
            """
            SELECT ROUND(
                SUM(
                    oi.quantity
                    * oi.unit_price
                ),
                2
            )
            FROM orders AS o
            JOIN order_items AS oi
                ON oi.order_id = o.order_id
            WHERE o.status = 'completed'
            """
        ).fetchone()[0]

        self.assertEqual(revenue, 515.0)

    def test_refunded_order_is_excluded(self):
        rows = run_sql_file(
            self.connection,
            ROOT / "queries"
            / "monthly_revenue.sql",
        )

        values = {
            row["month"]: row["revenue"]
            for row in rows
        }

        self.assertEqual(
            values,
            {
                "2026-08": 325.0,
                "2026-09": 190.0,
            },
        )

    def test_customer_value_uses_window_rank(self):
        rows = run_sql_file(
            self.connection,
            ROOT / "queries"
            / "customer_value.sql",
        )

        self.assertEqual(
            rows[0]["customer_id"],
            "C001",
        )
        self.assertEqual(
            rows[0]["revenue"],
            200.0,
        )
        self.assertEqual(
            rows[0]["revenue_rank"],
            1,
        )

    def test_category_margin_is_known(self):
        rows = run_sql_file(
            self.connection,
            ROOT / "queries"
            / "category_margin.sql",
        )

        by_category = {
            row["category"]: row
            for row in rows
        }

        self.assertEqual(
            by_category["peripheral"]["revenue"],
            440.0,
        )
        self.assertEqual(
            by_category["accessory"]["revenue"],
            75.0,
        )
        self.assertEqual(
            by_category["peripheral"]["gross_margin"],
            170.0,
        )

    def test_foreign_key_is_enforced(self):
        with self.assertRaises(
            sqlite3.IntegrityError
        ):
            self.connection.execute(
                """
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    ordered_at,
                    status
                )
                VALUES (
                    99,
                    'MISSING',
                    '2026-10-01',
                    'completed'
                )
                """
            )

    def test_quantity_constraint_is_enforced(self):
        with self.assertRaises(
            sqlite3.IntegrityError
        ):
            self.connection.execute(
                """
                INSERT INTO order_items (
                    order_id,
                    line_no,
                    product_id,
                    quantity,
                    unit_price
                )
                VALUES (
                    1,
                    99,
                    'P001',
                    0,
                    100
                )
                """
            )


if __name__ == "__main__":
    unittest.main()
