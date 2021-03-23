CREATE VIEW features_summary AS

SELECT reviews.products_id, reviews.sentiment, count(reviews.feature_names_id) AS quantity
FROM (reviews
JOIN feature_names USING (feature_names_id))
GROUP BY reviews.products_id, reviews.sentiment;