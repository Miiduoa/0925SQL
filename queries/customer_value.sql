WITH customer_sales AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(DISTINCT o.order_id) AS completed_orders,
        ROUND(
            SUM(oi.quantity * oi.unit_price),
            2
        ) AS revenue,
        MAX(o.ordered_at) AS last_order_date
    FROM customers AS c
    JOIN orders AS o
        ON o.customer_id = c.customer_id
       AND o.status = 'completed'
    JOIN order_items AS oi
        ON oi.order_id = o.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
)
SELECT
    customer_id,
    customer_name,
    completed_orders,
    revenue,
    last_order_date,
    DENSE_RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM customer_sales
ORDER BY revenue_rank, customer_id;
