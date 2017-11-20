drop table words if exists;
CREATE TABLE
 IF NOT EXISTS words (
    id integer PRIMARY KEY,
    name text NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop table scores if exists;
CREATE TABLE
 IF NOT EXISTS scores (
    id integer PRIMARY KEY,
    word text NOT NULL,
    spelling text NULL,
    answer integer not null,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);
