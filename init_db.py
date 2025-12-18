import sqlite3
import os

# Configuration
DB_FILE = 'data/school_management.db'
SCHEMA_FILE = 'data/schema.sql'

def init_db():
    # 1. Check if schema file exists
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ ERROR: Schema file not found at {SCHEMA_FILE}")
        return

    # 2. Connect (This creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        # 3. Read the SQL schema
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        
        # 4. Execute the script
        # executescript() is special: it runs multiple SQL commands at once
        cur.executescript(sql_script)
        
        conn.commit()
        print(f"✅ SUCCESS: Database created at '{DB_FILE}'")
        print("   All tables initialized successfully.")

    except sqlite3.Error as e:
        print(f"❌ DATABASE ERROR: {e}")
    
    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")
        
    finally:
        conn.close()

if __name__ == '__main__':
    # Warn the user before wiping
    if os.path.exists(DB_FILE):
        response = input(f"⚠️  WARNING: '{DB_FILE}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            exit()
        os.remove(DB_FILE) # Ruthless clean start
    
    init_db()