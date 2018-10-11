#!/usr/bin/env bash



data_dir="../zoo_server/data"

zoo_path="${data_dir}/zoo_data.txt"
monkey_path="${data_dir}/monkey_data.txt"

if [ ! -e $zoo_path ]; then
    echo "did not provide a correct argument for path to data";
    exit;
fi


eval "$(./export_db_values.sh)"

./drop_all.sh


mysql -h${host} -u${user} ${db} < create_tables.sql

function prepare_values {
    out=${1//,/\",\"}
    echo "(\"${out}\")"
}

readarray -t zoo_lines < $zoo_path
for el in "${zoo_lines[@]}"; do
    if [[ $el != \#* ]]; then
        values="$(prepare_values "$el")"
        mysql -h${host} -u${user} ${db} -e "INSERT INTO zoo (name, opens, closes) VALUES $values;"
    fi
done



mysql -h${host} -u${user} ${db} -e "DROP TABLE IF EXISTS temp_monkey;"

mysql -h${host} -u${user} ${db} -e " 
CREATE TABLE temp_monkey (
    temp_name VARCHAR(20) NOT NULL,
    temp_sex ENUM('M', 'F') NOT NULL,
    temp_flings_poop ENUM('TRUE', 'FALSE') NOT NULL,
    temp_poop_size INT NOT NULL,
    temp_zoo_name VARCHAR(50)
);
"


readarray -t monkey_lines < $monkey_path

for el in "${monkey_lines[@]}"; do
    if [[ $el != \#* ]]; then
        values="$(prepare_values "$el")"
        mysql -h${host} -u${user} ${db} -e "
        INSERT INTO temp_monkey 
            (temp_name, temp_sex, temp_flings_poop, temp_poop_size, temp_zoo_name) 
        VALUES $values;"
    fi
done

mysql -h${host} -u${user} ${db} -e "
INSERT INTO monkey (name, sex, flings_poop, poop_size, zoo_id) 
SELECT 
    temp_name, temp_sex, 
    (temp_flings_poop='TRUE'), 
    temp_poop_size, zoo.id 
FROM temp_monkey, zoo   
    WHERE temp_zoo_name = zoo.name;"

mysql -h${host} -u${user} ${db} -e "DROP TABLE temp_monkey;"


