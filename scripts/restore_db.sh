#!/bin/bash

# restore_db.sh - Script to restore latest PostgreSQL database dump

# Ensure we're running from the project root
cd "$(dirname "$0")/.." || exit 1

echo "Starting database restore process..."

# Check if pg_restore is installed
if ! command -v pg_restore &> /dev/null; then
    echo "Error: pg_restore is not installed or not in PATH."
    echo ""
    echo "Please install PostgreSQL client tools:"
    echo "  Ubuntu/Debian: sudo apt-get install postgresql-client"
    echo "  macOS (Homebrew): brew install libpq"
    echo "  macOS (Postgres.app): Ensure /Applications/Postgres.app/Contents/Versions/latest/bin is in your PATH."
    echo "  Windows: Install PostgreSQL and add the bin directory to your PATH."
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found in the project root. Make sure database credentials are set in your environment."
fi

# Set default values if not provided by .env
PGUSER="${POSTGRES_USER:-user}"
PGPASSWORD="${POSTGRES_PASSWORD:-password}"
PGDATABASE="${POSTGRES_DB:-thoughts}"
PGHOST="${POSTGRES_HOST:-localhost}"
PGPORT="${POSTGRES_PORT:-5432}"

BACKUP_DIR="data_backups"

if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
    echo "Error: No backups found in the '$BACKUP_DIR' directory."
    exit 1
fi

# Find the latest .dump file
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.dump | head -n1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "Error: No backup files (.dump) found in the '$BACKUP_DIR' directory."
    exit 1
fi

echo "Found latest backup: $LATEST_BACKUP"
echo ""
echo "⚠️ WARNING: Proceeding will DROP existing objects in the '${PGDATABASE}' database and RESTORE from the backup."
read -p "Are you sure you want to proceed? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Database restore cancelled."
    exit 0
fi

echo "Restoring database '${PGDATABASE}' from $LATEST_BACKUP..."

# Export PGPASSWORD so pg_restore doesn't prompt for it
export PGPASSWORD

# Run pg_restore
# -c: clean (drop) database objects before recreating
# -Fc: custom format
if pg_restore -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c -Fc "$LATEST_BACKUP"; then
    echo "✅ Database restore completed!"
else
    echo "⚠️ Database restore finished with some errors (check above output), but most standard restore operations may still be largely successful if the database state is usable."
fi
