CREATE VIEW products_count AS

SELECT * FROM
( 
SELECT product_categories_id, czech_name,ang.name english_name , all_products, coalesce(new_products,0) new_products
FROM product_categories LEFT JOIN (SELECT  product_categories_id, count(*) all_products FROM products GROUP BY product_categories_id)ap USING (product_categories_id) LEFT JOIN (
SELECT product_categories_id product_categories_id, count(*) new_products FROM products  WHERE inserted_at > current_date - interval '7 days' GROUP BY product_categories_id) np USING (product_categories_id) LEFT JOIN
(SELECT product_categories_id, name FROM product_category_names WHERE languages_id=2)ang USING (product_categories_id)
UNION
SELECT 0, 'vše' , 'all products', all_products, new_products 
FROM  (SELECT  count(*) all_products FROM products)ap,
      (SELECT  count(*) new_products FROM products  WHERE inserted_at > current_date - interval '7 days')np

)xxx
ORDER BY product_categories_id	
