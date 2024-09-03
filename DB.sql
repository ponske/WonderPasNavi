CREATE DATABASE wonderpasnavi;
CREATE USER wpnuser WITH PASSWORD '***';
GRANT ALL PRIVILEGES ON DATABASE wonderpasnavi TO wpnuser;
\c wonderpasnavi

CREATE TABLE attraction(
    id INT,
    park VARCHAR(4),
    name VARCHAR(100),
    area VARCHAR(50)
);
GRANT SELECT, INSERT, UPDATE, DELETE ON attraction TO wpnuser;


CREATE TABLE trk_waitingtime(
    data_id SERIAL PRIMARY KEY,
    attr_id INT,
    waitingperiod INT,
    at_t TIMESTAMP
);
GRANT SELECT, INSERT, UPDATE, DELETE ON trk_waitingtime TO wpnuser;
GRANT USAGE ON SEQUENCE trk_waitingtime_data_id_seq TO wpnuser;

CREATE TABLE trk_operation(
    data_id SERIAL PRIMARY KEY,
    attr_id INT,
    condition VARCHAR(100),
    at_t TIMESTAMP
);
GRANT SELECT, INSERT, UPDATE, DELETE ON trk_operation TO wpnuser;
GRANT USAGE ON SEQUENCE trk_operation_data_id_seq TO wpnuser;