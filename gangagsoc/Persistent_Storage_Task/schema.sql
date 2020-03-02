CREATE DATABASE IF NOT EXISTS job;
USE job;
CREATE  TABLE IF NOT EXISTS `data` (`id` int NOT NULL AUTO_INCREMENT, `attributes` BLOB, `job_string_blob` BLOB, PRIMARY KEY (`id`));
CREATE USER 'ganga'@'localhost' IDENTIFIED BY 'Ganga_2020';
GRANT ALL PRIVILEGES ON *.* TO 'ganga'@'localhost';