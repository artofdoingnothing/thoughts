import sys
import os

# Add the project root to sys.path to allow importing from libs
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Default to local postgres if not set
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "postgresql://user:password@localhost:5432/thoughts"

from libs.db_service.models import SessionLocal, Thought

TARGET_TEXTS = [
    "➡️ Toggle dark mode 🌗\n    \n➡️ Subscribe via a feeds reader:\n      RSS,\n      Atom",
    "➡️ Toggle dark mode 🌗"
]

def main():
    session = SessionLocal()
    try:
        total_deleted = 0
        for text in TARGET_TEXTS:
            print(f"Searching for thoughts containing: {repr(text)}")
            # Filter specifically for the persona and text if needed, 
            # but user said "any" thoughts.
            query = session.query(Thought).filter(Thought.content.contains(text))
            thoughts_to_delete = query.all()
            count = len(thoughts_to_delete)
            
            if count > 0:
                print(f"Found {count} thoughts to delete for this pattern.")
                for t in thoughts_to_delete:
                    session.delete(t)
                total_deleted += count
            else:
                print("No thoughts found for this pattern.")
        
        if total_deleted > 0:
            session.commit()
            print(f"Successfully deleted {total_deleted} thoughts in total.")
        else:
            print("No thoughts deleted.")
        
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
