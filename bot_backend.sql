CREATE DATABASE dicebag;
\c dicebag;

DROP TABLE IF EXISTS names;
CREATE TABLE names(
    id serial,
    name text not null,
    race text not null,
    category char(1) not null,
    primary key(id)
);

INSERT INTO names (name, race, category) VALUES ('Jeelius', 'argonian', 'm');

