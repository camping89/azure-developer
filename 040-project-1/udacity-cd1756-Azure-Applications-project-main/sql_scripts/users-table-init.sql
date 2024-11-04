-- Drop existing table if it exists
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL
    DROP TABLE dbo.users;

-- Create new users table with all fields
CREATE TABLE users (
    id INT NOT NULL IDENTITY(1, 1),
    username VARCHAR(64) NOT NULL,
    password_hash VARCHAR(256),
    ms_id VARCHAR(200),
    email VARCHAR(120),
    name VARCHAR(120),
    is_microsoft_auth BIT DEFAULT 0,
    PRIMARY KEY (id)
);

-- Create indexes
CREATE UNIQUE INDEX ix_users_username ON users(username);
CREATE UNIQUE INDEX ix_users_ms_id ON users(ms_id) WHERE ms_id IS NOT NULL;
CREATE UNIQUE INDEX ix_users_email ON users(email) WHERE email IS NOT NULL;

-- Insert default admin user
INSERT INTO dbo.users (username, password_hash, is_microsoft_auth)
VALUES (
    'admin',
    'pbkdf2:sha256:150000$QlIrz6Hg$5f4cd25d78a6c79906a53f74ef5d3bb2609af2b39d9944ac336c07f9e3be8d58',
    0
);