# ENVIRONMENT YOU HAVE TO WRITE INSIDE YOUR .env FILE
# DATABASE 
- DBMS for example postgresql+psycopg
- WARNING!!! There is "postgresql_user" in docker-compose in "test: [ 'CMD-SHELL', 'pg_isready -U postgresql_user' ]". Rewrite it on your DB_USER
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_HOST_TEST db host for testing(pytest)
- DB_NAME
- DB_NAME_TEST db name for testing(pytest)
# JWT
- SECRET_KEY write "openssl rand -hex 32" to get it
- ALGORITHM for example HS256
- EXPIRE_TIME_MINUTES 
