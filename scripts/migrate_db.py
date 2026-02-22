import os
import alembic.config
import alembic.command
from alembic.script import ScriptDirectory

def run_migrations():
    alembic_cfg = alembic.config.Config("alembic.ini")
    
    # Check if there are any existing revisions
    script = ScriptDirectory.from_config(alembic_cfg)
    revisions = list(script.walk_revisions())
    
    if not revisions:
        print("No revisions found. Generating initial migration...")
        try:
            alembic.command.revision(alembic_cfg, message="Initial migration", autogenerate=True)
        except Exception as e:
            print(f"Error generating revision: {e}")
            # Ensure we don't crash if it's just that there are no changes or connection issue, 
            # but usually we want to know.
            pass
    
    print("Running migrations...")
    try:
        alembic.command.upgrade(alembic_cfg, "head")
        print("Migrations complete.")
    except Exception as e:
        print(f"Error running migrations: {e}")
        raise e

if __name__ == "__main__":
    run_migrations()
