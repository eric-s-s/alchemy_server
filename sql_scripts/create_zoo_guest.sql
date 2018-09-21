DROP USER IF EXISTS 'zoo_guest'@'localhost' ;
CREATE USER 'zoo_guest'@'localhost';
GRANT ALL PRIVILEGES ON zoo.* TO 'zoo_guest'@'localhost';
GRANT FILE ON *.* TO 'zoo_guest'@'localhost';
