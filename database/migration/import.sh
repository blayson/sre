#!/usr/bin/env bash
# import standardni DB

# Terminate all existing connections
psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
						WHERE pg_stat_activity.datname = 'mta' AND pid <> pg_backend_pid();"

# Recreate tables
psql -U postgres -c "DROP DATABASE IF EXISTS mta;"
psql -U postgres -c "CREATE DATABASE mta;"

# # Set timezone
# psql -U postgres mta -c "SET TIME ZONE 'Europe/Prague';"

psql -U postgres mta -f "/tmp/db/create_tables.sql"
psql -U postgres mta -f "/tmp/db/import_languages.sql"
psql -U postgres mta -f "/tmp/db/20191004_user_reviews.sql"
psql -U postgres mta -f "/tmp/db/20191024_mta_score.sql"
psql -U postgres mta -f "/tmp/db/20191101_uprava_databaze_product_reviews.sql"
psql -U postgres mta -f "/tmp/db/20191108_uprava_tabulky_products.sql"
psql -U postgres mta -f "/tmp/db/import_users.sql"
psql -U postgres mta -f "/tmp/db/import_product_categories.sql"
psql -U postgres mta -f "/tmp/db/import_product_category_names.sql"
psql -U postgres mta -f "/tmp/db/import_feature_names.sql"
psql -U postgres mta -f "/tmp/db/import_products.sql"
psql -U postgres mta -f "/tmp/db/import_product_names.sql"
psql -U postgres mta -f "/tmp/db/import_reviews.sql"
psql -U postgres mta -f "/tmp/db/import_product_characteristics.sql"
psql -U postgres mta -f "/tmp/db/20191106_insert_units_characteristics.sql"
psql -U postgres mta -f "/tmp/db/20191129_feature_names_description.sql"
psql -U postgres mta -f "/tmp/db/20200205_product_articles.sql"
psql -U postgres mta -f "/tmp/db/20200312_suggestions.sql"
psql -U postgres mta -f "/tmp/db/20200422_reviews_suggestions_states.sql"
psql -U postgres mta -f "/tmp/db/20200327_sample_articles.sql"
psql -U postgres mta -f "/tmp/db/20200430_Doplneni_jazyka_do_tabulky__product_articles.sql"
psql -U postgres mta -f "/tmp/db/20200507_zmeny_v_tabulce_products.sql"
psql -U postgres mta -f "/tmp/db/20200618_product_features_keywords.sql"
psql -U postgres mta -f "/tmp/db/20200703_pridani_sloupce.sql"
psql -U postgres mta -f "/tmp/db/import_product_features_keywords.sql"
psql -U postgres mta -f "/tmp/db/20200724_nove_sloupce.sql"
psql -U postgres mta -f "/tmp/db/20200731_null_product_features_keywords.sql"
psql -U postgres mta -f "/tmp/db/import_favourites.sql"
psql -U postgres mta -f "/tmp/db/import_user_reviews.sql"
psql -U postgres mta -f "/tmp/db/20201008_reviews_ngrams.sql"
psql -U postgres mta -f "/tmp/db/20201113_view_products_count.sql"
psql -U postgres mta -f "/tmp/db/20201113_view_reviews_count.sql"
psql -U postgres mta -f "/tmp/db/20201208_view_features_summary.sql"
