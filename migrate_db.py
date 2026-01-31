from peewee import SqliteDatabase, BooleanField, PostgresqlDatabase
from playhouse.migrate import *
from playhouse.db_url import connect
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///thoughts.db")
db = connect(DB_URL)

if isinstance(db, PostgresqlDatabase):
    migrator = PostgresqlMigrator(db)
else:
    migrator = SqliteMigrator(db)

# Ensure tables exist
from libs.db_service.models import init_db
init_db()

is_generated_field = BooleanField(default=False)

def run_migration():
    print(f"Migrating database at {DB_URL}...")
    try:
        with db.transaction():
            migrate_ops = []
            
            # Check if columns exist before adding (basic check by trying to access, or just add and catch error)
            # Simpler to just attempt adding.
            
            try:
                migrate_ops.append(migrator.add_column('thought', 'is_generated', is_generated_field))
                print("Added is_generated to Thought.")
            except Exception as e:
                print(f"Skipping Thought.is_generated: {e}")

            try:
                migrate_ops.append(migrator.add_column('thoughttag', 'is_generated', is_generated_field))
                print("Added is_generated to ThoughtTag.")
            except Exception as e:
                print(f"Skipping ThoughtTag.is_generated: {e}")

            try:
                migrate_ops.append(migrator.add_column('thoughtemotion', 'is_generated', is_generated_field))
                print("Added is_generated to ThoughtEmotion.")
            except Exception as e:
                print(f"Skipping ThoughtEmotion.is_generated: {e}")

            if migrate_ops:
                migrate(*migrate_ops)
                print("Migration complete.")
            else:
                print("No migrations to run.")
                
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
