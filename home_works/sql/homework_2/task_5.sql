SELECT COUNT(products.product_id) AS total_products,
       AVG(products.price) AS average_price,
       supplier.supplier_name as supplier
FROM products
LEFT JOIN supplier
    ON products.supplier_id = supplier.supplier_id
GROUP BY supplier.supplier_id;