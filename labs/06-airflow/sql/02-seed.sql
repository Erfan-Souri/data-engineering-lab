INSERT INTO lab.customer_orders
(
    customer_name,
    category,
    payment_method,
    amount,
    status,
    created_at
)
SELECT

    ------------------------------------------------------------------
    -- 500 unique customers
    ------------------------------------------------------------------

    'Customer-' || LPAD((1 + floor(random() * 500))::TEXT, 4, '0'),

    ------------------------------------------------------------------
    -- Product Category
    ------------------------------------------------------------------

    (
        ARRAY[
            'Electronics',
            'Books',
            'Clothing',
            'Home',
            'Sports',
            'Beauty'
        ]
    )[1 + floor(random()*6)::int],

    ------------------------------------------------------------------
    -- Payment Method
    ------------------------------------------------------------------

    (
        ARRAY[
            'Credit Card',
            'Debit Card',
            'Bank Transfer',
            'Digital Wallet',
            'Cash On Delivery'
        ]
    )[1 + floor(random()*5)::int],

    ------------------------------------------------------------------
    -- Amount
    -- 70% small
    -- 25% medium
    -- 5% large
    ------------------------------------------------------------------

    CASE

        WHEN random() < 0.70 THEN
            ROUND((20 + random() * 180)::numeric,2)

        WHEN random() < 0.95 THEN
            ROUND((200 + random() * 800)::numeric,2)

        ELSE
            ROUND((1000 + random() * 4000)::numeric,2)

    END,

    ------------------------------------------------------------------
    -- Status
    ------------------------------------------------------------------

    CASE

        WHEN random() < 0.82 THEN 'completed'
        WHEN random() < 0.92 THEN 'pending'
        WHEN random() < 0.97 THEN 'cancelled'
        ELSE 'refunded'

    END,

    ------------------------------------------------------------------
    -- Random date during last 180 days
    ------------------------------------------------------------------

    NOW()
        - (
            floor(random() * 180)
            * INTERVAL '1 day'
          )
        - (
            floor(random() * 86400)
            * INTERVAL '1 second'
          )

FROM generate_series(1,10000);