CREATE TABLE zoo (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    opens TIME NOT NULL,
    closes TIME NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE monkey (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    sex ENUM('m', 'f') NOT NULL,
    flings_poop BOOL NOT NULL,
    poop_size INT NOT NULL,
    zoo_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (zoo_id)
        REFERENCES zoo(id)
        ON DELETE CASCADE
);

CREATE INDEX monkey_name ON monkey (name);

CREATE INDEX zoo_name ON zoo (name);

