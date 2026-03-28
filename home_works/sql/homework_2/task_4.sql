SELECT COUNT(`order`.product_id) as total
FROM `order`
    LEFT JOIN products
        ON `order`.product_id = products.product_id
WHERE products.price BETWEEN 20 AND 100;