sql_scripts/drop_all.sh
mysql -u zoo_guest zoo < sql_scripts/create_tables.sql
python3 load_test_data.py
