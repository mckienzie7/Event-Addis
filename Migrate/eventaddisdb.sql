DROP DATABASE IF EXISTS eventaddis_db;


--Creating the database for Event addis

CREATE  DATABASE IF NOT EXISTS eventaddist_db;
CREATE USER IF NOT EXISTS 'adminx'@'localhost';
SET PASSWORD FOR 'adminx'@'localhost' = 'XXXXXXX';
GRANT ALL ON eventaddis_db.* TO 'adminx'@'localhost';
GRANT SELECT ON performance_schema.* TO 'adminx'@'localhost';
FLUSH PRIVILEGES;