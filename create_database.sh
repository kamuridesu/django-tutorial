docker cp ./db.sql dj_postgres:/var/lib/postgresql
docker exec -it -u postgres dj_postgres psql -f /var/lib/postgresql/db.sql