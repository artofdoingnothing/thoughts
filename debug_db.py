import os

# Force local connection for debugging script ONLY if not already set
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://user:password@localhost:5432/thoughts"

from libs.db_service.models import Thought, ThoughtTag, ThoughtEmotion, Tag, Emotion, db

def query_thoughts():
    if db.is_closed():
        db.connect()
    
    thoughts = Thought.select()
    count = thoughts.count()
    print(f"Total thoughts found: {count}")
    print("-" * 30)

    for t in thoughts:
        print(f"ID: {t.id}")
        print(f"Title: {t.title}")
        print(f"Content: {t.content}")
        print(f"Status: {t.status}")
        print(f"Is Generated: {t.is_generated}")
        
        print("Tags:")
        tags = [f"{tt.tag.name} (auto={tt.is_generated})" for tt in t.tags]
        if tags:
            for tag in tags:
                print(f"  - {tag}")
        else:
            print("  (No tags)")
            
        print("Emotions:")
        emotions = [f"{te.emotion.name} (auto={te.is_generated})" for te in t.emotions]
        if emotions:
            for emotion in emotions:
                print(f"  - {emotion}")
        else:
            print("  (No emotions)")
        print("-" * 30)

if __name__ == "__main__":
    try:
        query_thoughts()
    except Exception as e:
        print(f"Error querying database: {e}")
