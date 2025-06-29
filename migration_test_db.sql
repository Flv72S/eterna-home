BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 0a43c1e9241f

CREATE TABLE "user" (
    id SERIAL NOT NULL, 
    email VARCHAR NOT NULL, 
    username VARCHAR, 
    hashed_password VARCHAR NOT NULL, 
    full_name VARCHAR, 
    phone_number VARCHAR, 
    is_active BOOLEAN NOT NULL, 
    is_superuser BOOLEAN NOT NULL, 
    is_verified BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    last_login TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    UNIQUE (username)
);

CREATE UNIQUE INDEX ix_user_email ON "user" (email);

CREATE TABLE house (
    id SERIAL NOT NULL, 
    owner_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(owner_id) REFERENCES "user" (id)
);

CREATE TABLE booking (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id)
);

INSERT INTO alembic_version (version_num) VALUES ('0a43c1e9241f') RETURNING alembic_version.version_num;

COMMIT;

