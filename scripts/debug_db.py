import os
import sys

# Ensure the root of the project is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Force local connection for debugging script if not already set
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://user:password@localhost:5432/thoughts"

from libs.db_service.models import SessionLocal, Tag, Thought, ThoughtTag

def debug_data():
    session = SessionLocal()
    try:
        print("Querying Thoughts...")
        thoughts = session.query(Thought).all()
        print(f"Total thoughts found: {len(thoughts)}")
        for t in thoughts:
            print(f"ID: {t.id} | Title: {t.title if hasattr(t, 'title') else 'No Title'} | Generated: {t.is_generated}")
            tags = session.query(ThoughtTag).filter(ThoughtTag.thought_id == t.id).all()
            if tags:
                print(f"  Tags: {[tag.tag_id for tag in tags]}") # Just IDs for now to avoid lazy load issues if Tag not joined
            else:
                print("  (No tags)")
        
        print("-" * 30)
        print("Querying Tags (Global)...")
        tags = session.query(Tag).all()
        print(f"Total global tags found: {len(tags)}")
        for tag in tags:
            print(f"ID: {tag.id}, Name: {tag.name}")
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    debug_data()
