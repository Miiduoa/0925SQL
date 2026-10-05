INSERT INTO customers (
    customer_id,
    customer_name,
    segment
) VALUES
    ('C001', 'North Studio', 'business'),
    ('C002', 'Chen', 'consumer'),
    ('C003', 'Campus Lab', 'education');

INSERT INTO products (
    product_id,
    product_name,
    category,
    unit_cost
) VALUES
    ('P001', 'Keyboard', 'peripheral', 60.0),
    ('P002', 'Mouse', 'peripheral', 30.0),
    ('P003', 'USB Hub', 'accessory', 15.0);

INSERT INTO orders (
    order_id,
    customer_id,
    ordered_at,
    status
) VALUES
    (1, 'C001', '2026-08-03', 'completed'),
    (2, 'C002', '2026-08-10', 'completed'),
    (3, 'C001', '2026-09-02', 'refunded'),
    (4, 'C003', '2026-09-15', 'completed');

INSERT INTO order_items (
    order_id,
    line_no,
    product_id,
    quantity,
    unit_price
) VALUES
    (1, 1, 'P001', 1, 100.0),
    (1, 2, 'P002', 2, 50.0),
    (2, 1, 'P002', 1, 50.0),
    (2, 2, 'P003', 3, 25.0),
    (3, 1, 'P001', 1, 100.0),
    (4, 1, 'P001', 2, 95.0);
