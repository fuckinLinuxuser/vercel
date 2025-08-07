CREATE ROLE botuser WITH LOGIN PASSWORD '819219';
ALTER ROLE botuser SET client_encoding TO 'utf8';
ALTER ROLE botuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE botuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE botdb TO botuser;
