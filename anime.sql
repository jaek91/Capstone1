CREATE TABLE anime_db
(anime_id INT PRIMARY KEY, "name" TEXT, genre TEXT, "type" TEXT, episodes INT, 
rating DOUBLE PRECISION, members INT);

COPY anime_db FROM  '/mnt/c/Springboard/Capstone_1/anime.csv' WITH (FORMAT CSV, DELIMITER ',', HEADER);
