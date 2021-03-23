CREATE VIEW reviews_count AS
SELECT * FROM
( 
   SELECT product_categories_id, czech_name,ang.name english_name , coalesce(all_reviews,0) all_reviews, coalesce(new_reviews,0) new_reviews
   FROM product_categories LEFT JOIN 
        (SELECT  product_categories_id, count(*) all_reviews FROM products JOIN reviews USING (products_id) GROUP BY product_categories_id)ap USING (product_categories_id) LEFT JOIN 
        (SELECT product_categories_id product_categories_id, count(*) new_reviews FROM products JOIN reviews USING (products_id) WHERE reviews.inserted_at > current_date - interval '7 days' GROUP BY product_categories_id) np USING (product_categories_id) LEFT JOIN
        (SELECT product_categories_id, name FROM product_category_names WHERE languages_id=2)ang USING (product_categories_id)
   UNION
   SELECT 0, 'vše' , 'all products', all_reviews, new_reviews 
   FROM (SELECT  count(*) all_reviews FROM products JOIN reviews USING (products_id))ap,
        (SELECT  count(*) new_reviews FROM products JOIN reviews USING (products_id) WHERE reviews.inserted_at > current_date - interval '7 days')np

)xxx
ORDER BY product_categories_id	
