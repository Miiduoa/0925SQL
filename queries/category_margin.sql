SELECT
    p.category,
    SUM(oi.quantity) AS units,
    ROUND(
        SUM(oi.quantity * oi.unit_price),
        2
    ) AS revenue,
    ROUND(
        SUM(
            oi.quantity * (
                oi.unit_price - p.unit_cost
            )
        ),
        2
    ) AS gross_margin,
    ROUND(
        SUM(
            oi.quantity * (
                oi.unit_price - p.unit_cost
            )
        )
        / NULLIF(
            SUM(oi.quantity * oi.unit_price),
            0
        ),
        4
    ) AS margin_rate
FROM orders AS o
JOIN order_items AS oi
    ON oi.order_id = o.order_id
JOIN products AS p
    ON p.product_id = oi.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;
