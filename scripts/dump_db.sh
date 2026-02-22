#!/bin/bash

# dump_db.sh - Script to create a PostgreSQL database dump

# Ensure we're running from the project root
cd "$(dirname "$0")/.." || exit 1

echo "Starting database backup process..."

# Check if pg_dump is installed
if ! command -v pg_dump &> /dev/null; then
    echo "Error: pg_dump is not installed or not in PATH."
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

# Create backup directory if it doesn't exist
BACKUP_DIR="data_backups"
mkdir -p "$BACKUP_DIR"

# Generate timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${TIMESTAMP}.dump"

echo "Creating dump for database '${PGDATABASE}' at ${PGHOST}:${PGPORT}..."

# Export PGPASSWORD so pg_dump doesn't prompt for it
export PGPASSWORD

# Run pg_dump (custom format -Fc is generally best for restores)
if pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -Fc -f "$BACKUP_FILE" "$PGDATABASE"; then
    echo "✅ Database backup successful!"
    echo "Backup saved to: $BACKUP_FILE"
else
    echo "❌ Database backup failed."
    exit 1
fi
