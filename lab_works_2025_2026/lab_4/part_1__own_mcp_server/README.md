# How to run the code

# I. Create & validate creation of Postgres database

1. Go to this dirrectory in your console.
2. Run command: `docker compose up -d`
3. Validate with command: `docker exec -e PGPASSWORD='M&1_V3r^_C9#pLeX_P@$s' -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`
4. P.s. without pass it also works: `docker exec -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`,
   but I've kept the pass for possible testings.

# II. Create own 