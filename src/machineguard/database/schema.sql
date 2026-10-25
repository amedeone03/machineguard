CREATE TABLE bearings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    experiment VARCHAR(100),
    channel VARCHAR(50)
);

CREATE TABLE measurements (
    id SERIAL PRIMARY KEY,
    bearing_id INTEGER NOT NULL REFERENCES bearings(id),
    timestamp TIMESTAMP NOT NULL,

    rms DOUBLE PRECISION,
    std DOUBLE PRECISION,
    peak DOUBLE PRECISION,
    crest_factor DOUBLE PRECISION,
    kurtosis DOUBLE PRECISION,
    dominant_frequency DOUBLE PRECISION,
    spectral_energy DOUBLE PRECISION,

    anomaly_score DOUBLE PRECISION,
    anomaly_flag BOOLEAN,

    UNIQUE (bearing_id, timestamp)
);