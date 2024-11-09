DROP DATABASE IF EXISTS eventaddis_db;




CREATE  DATABASE IF NOT EXISTS eventaddis_db;
CREATE USER IF NOT EXISTS 'EAadmin'@'localhost';
SET PASSWORD FOR 'EAadmin'@'localhost' = 'Mckienzie12';
GRANT ALL ON eventaddis_db.* TO 'EAadmin'@'localhost';
DROP DATABASE IF EXISTS eventaddis_db;
CREATE  DATABASE IF NOT EXISTS eventaddis_db;
GRANT SELECT ON performance_schema.* TO 'EAadmin'@'localhost';
FLUSH PRIVILEGES;