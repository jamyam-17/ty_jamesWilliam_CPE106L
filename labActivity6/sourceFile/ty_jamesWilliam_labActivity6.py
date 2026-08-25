import sqlite3

def setup_database():
    # Create/Connect SQL file
    conn = sqlite3.connect('literature_manager.db')
    cursor = conn.cursor()

    # Create columns of table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            url TEXT,
            abstract TEXT,
            methods TEXT,
            results TEXT,
            read_status TEXT DEFAULT 'To Read'
        )
    ''')
    
    # Add sample data
    cursor.execute("SELECT COUNT(*) FROM articles")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            (
                "IEEE Document 11219194",
                "IEEE Author",
                "https://ieeexplore.ieee.org/document/11219194",
                "SAMPLE ABSTRACT",
                "Experimental analysis",
                "Positive results achieved."
            ),
            (
                "IEEE Document 10346798",
                "IEEE Author",
                "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10346798",
                "SAMPLE ABSTRACT",
                "Computational modeling",
                "Model accuracy improved."
            )
        ]
        
        cursor.executemany('''
            INSERT INTO articles (title, author, url, abstract, methods, results)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)
        conn.commit()
        
    return conn

def main():
    conn = setup_database()
    cursor = conn.cursor()
    
    while True:
        print("\nLiterature Review Manager")
        print("1. View Short List of Articles")
        print("2. View Specific Article (Full Details)")
        print("3. Add New Article")
        print("4. Edit Article Status")
        print("5. Delete Article")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '1':
            cursor.execute("SELECT article_id, read_status, title, url, abstract FROM articles ORDER BY article_id ASC")
            records = cursor.fetchall()
            print(f"\n{'-'*145}")
            print(f"{'ID':<4} | {'Status':<10} | {'Title':<45} | {'URL':<50} | {'Abstract'}")
            print("-" * 145)
            if not records:
                print("No articles found in the database.")
            for r in records:
                # Truncate long strings for cleaner terminal display
                title = r[2][:42] + "..." if len(r[2]) > 45 else r[2]
                url = r[3][:47] + "..." if len(r[3]) > 50 else r[3]
                abstract = r[4][:27] + "..." if len(r[4]) > 30 else r[4]
                print(f"{r[0]:<4} | {r[1]:<10} | {title:<45} | {url:<50} | {abstract}")
            print(f"{'-'*145}")
                
        elif choice == '2':
            try:
                article_id = int(input("Enter Article ID to view full details: "))
                cursor.execute("SELECT * FROM articles WHERE article_id = ?", (article_id,))
                article = cursor.fetchone()
                
                if article:
                    print(f"\n{'='*50}")
                    print(f"TITLE:   {article[1]}")
                    print(f"AUTHOR:  {article[2]}")
                    print(f"URL:     {article[3]}")
                    print(f"STATUS:  {article[7]}")
                    print(f"\nABSTRACT:\n{article[4]}")
                    print(f"\nMETHODS:\n{article[5]}")
                    print(f"\nRESULTS:\n{article[6]}")
                    print(f"{'='*50}")
                else:
                    print("** Article not found. **")
            except ValueError:
                print("** Error: Article ID must be a number. **")
            
        elif choice == '3':
            title = input("Title: ")
            author = input("Author(s): ")
            url = input("URL/DOI: ")
            abstract = input("Abstract: ")
            methods = input("Methods: ")
            results = input("Results: ")
            
            cursor.execute('''
                INSERT INTO articles (title, author, url, abstract, methods, results)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, url, abstract, methods, results))
            conn.commit()
            print(f"** '{title}' added to your local database! **")

        elif choice == '4':
            try:
                article_id = int(input("Enter Article ID to edit status: "))
                new_status = input("New Status (e.g., Read, Skimmed, To Read): ")
                cursor.execute("UPDATE articles SET read_status = ? WHERE article_id = ?", (new_status, article_id))
                conn.commit()
                print("** Status updated! **")
            except ValueError:
                print("** Error: Article ID must be a number. **")
                
        elif choice == '5':
            try:
                article_id = int(input("Enter Article ID to delete: "))
                cursor.execute("DELETE FROM articles WHERE article_id = ?", (article_id,))
                conn.commit()
                print("** Article deleted. **")
            except ValueError:
                print("** Error: Article ID must be a number. **")
                
        elif choice == '6':
            print("Closing the database. Happy researching!")
            cursor.close()
            conn.close()
            break
            
        else:
            print("** Invalid choice. Please select 1-6. **")

main()