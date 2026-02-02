from peewee import SqliteDatabase, BooleanField, PostgresqlDatabase, ForeignKeyField, IntegerField
from libs.db_service.models import Persona
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
# Avoid running full init_db() here as it might fail on index creation for missing columns
# init_db() 

is_generated_field = BooleanField(default=False)
persona_field = ForeignKeyField(Persona, field='id', backref='thoughts', null=True)

def run_migration():
    print(f"Migrating database at {DB_URL}...")
    
    # Create Persona table first as it's needed for FK
    try:
        db.create_tables([Persona], safe=True)
    except Exception as e:
        print(f"Error creating Persona table: {e}")

    # 1. Add is_generated to Thought
    try:
        with db.atomic():
            migrate(migrator.add_column('thought', 'is_generated', is_generated_field))
            print("Added is_generated to Thought.")
    except Exception as e:
        print(f"Skipping Thought.is_generated: {e}")

    # 2. Add is_generated to ThoughtTag
    try:
        with db.atomic():
            migrate(migrator.add_column('thoughttag', 'is_generated', is_generated_field))
            print("Added is_generated to ThoughtTag.")
    except Exception as e:
        print(f"Skipping ThoughtTag.is_generated: {e}")

    # 3. Add is_generated to ThoughtEmotion
    try:
        with db.atomic():
            migrate(migrator.add_column('thoughtemotion', 'is_generated', is_generated_field))
            print("Added is_generated to ThoughtEmotion.")
    except Exception as e:
        print(f"Skipping ThoughtEmotion.is_generated: {e}")

    # 4. Add persona_id to Thought
    try:
        with db.atomic():
            # Use IntegerField to avoid "Foreign-key has no attribute field_type" error in migration
            # We lose DB-level FK constraint enforcement for now but the app will work.
            f = IntegerField(null=True)
            migrate(migrator.add_column('thought', 'persona_id', f))
            print("Added persona_id to Thought.")
    except Exception as e:
         print(f"Skipping Thought.persona_id: {e}")
         
    print("Migration complete.")

if __name__ == "__main__":
    run_migration()
