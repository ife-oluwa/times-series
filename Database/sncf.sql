CREATE DATABASE my_db WITH TEMPLATE = template0 ENCODING = 'UTF8';
ALTER DATABASE my_db OWNER TO postgres;
DROP TABLE IF EXISTS sncf;
CREATE TABLE public.sncf (
    item_id serial PRIMARY KEY,
    date timestamp NOT NULL,
    return_date timestamp,
    gare varchar(255),
    item_cat varchar(255),
    item varchar(255),
    found_not_found varchar(255)
)