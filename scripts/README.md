# Administration Scripts

This directory contains various scripts for administration and maintenance.

## Database Scripts

These scripts provide utilities for creating custom-format database backups and restoring from them. They automatically source the database credentials defined in the `.env` file at the root of the project.

### Requirements

To run these scripts, you must install the PostgreSQL client tools on your host machine:

- **Ubuntu/Debian**: `sudo apt-get install postgresql-client`
- **macOS (Homebrew)**: `brew install libpq` (and follow instructions to add it to your PATH)
- **macOS (Postgres.app)**: Ensure `/Applications/Postgres.app/Contents/Versions/latest/bin` is in your PATH.
- **Windows**: Install PostgreSQL and ensure the `bin` directory is accessible in your PATH.

### 1. `dump_db.sh`

Creates a custom-format dump (`.dump`) of the PostgreSQL database.

**Usage:**

```bash
./scripts/dump_db.sh
```

**Behavior:**

- Creates a `data_backups/` directory in the project root if it doesn't exist.
- Executes `pg_dump` securely using the credentials from `.env`.
- Saves the dump file with a timestamp, e.g., `data_backups/20260221_143000.dump`.
- This folder is ignored by git.

### 2. `restore_db.sh`

Restores the database using the most recent backup available.

**Usage:**

```bash
./scripts/restore_db.sh
```

**Behavior:**

- Automatically finds the most recent `.dump` file inside the `data_backups/` directory.
- Prompts the user with a warning, since this operation will overwrite (drop and recreate) objects in the target database.
- Executes `pg_restore` with the custom format.

### Troubleshooting

- If the script fails indicating it cannot connect to the database, verify that your `.env` contains the correct `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, and `POSTGRES_PORT` variables.
- By default, if the host is missing, it will attempt to connect to `localhost:5432`. If you are running PostgreSQL inside Docker, make sure you are running the script from outside the container with port 5432 mapped.
