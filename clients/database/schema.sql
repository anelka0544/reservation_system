CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    workspace_id INTEGER REFERENCES workspaces(workspace_id),
    from_time TIMESTAMP NOT NULL,
    to_time TIMESTAMP NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mail VARCHAR(255) UNIQUE NOT NULL,
    hash_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN
);

CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    tariff_id INTEGER REFERENCES tariffs(tariff_id),
    location_id INTEGER REFERENCES locations(location_id),
    workspace_type VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(200) NOT NULL,
    building INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tariffs (
    tariff_id SERIAL PRIMARY KEY,
    hourly_rate DECIMAL(10,2) NOT NULL,
    daily_rate DECIMAL(10,2) NOT NULL,
    monthly_rate DECIMAL(10,2) NOT NULL
);