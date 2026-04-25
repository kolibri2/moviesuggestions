create table movies
(
    movie_key integer
        primary key autoincrement,
    movie_id  TEXT
        unique,
    title     TEXT,
    overview  TEXT,
    embedding BLOB
);

create table users
(
    user_id          INTEGER
        primary key autoincrement,
    username         TEXT not null
        unique,
    embedding_vector float
);

create table user_movie_preferences
(
    user_id     INTEGER not null
        references users,
    movie_key   INTEGER not null
        references movies,
    liked       INTEGER not null,
    movie_title TEXT    not null,
    timestamp   DATETIME default CURRENT_TIMESTAMP,
    primary key (user_id, movie_key),
    unique (user_id, movie_key),
    check (liked IN (0, 1))
);
