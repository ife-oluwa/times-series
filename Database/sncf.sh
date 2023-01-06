#! /bin/bash

set -e

psql -U"$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOF
    DROP TABLE IF EXISTS sncf;
    CREATE TABLE public.sncf (
    item_id int PRIMARY KEY,
    date timestamp NOT NULL,
    return_date timestamp,
    gare varchar(255),
    item_cat varchar(255),
    item varchar(255),
    found_not_found varchar(255)
);
EOF
