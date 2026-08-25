import sqlite3
from datetime import datetime

# Create database
conn = sqlite3.connect('workshop_inventory_final.db')
conn.execute("PRAGMA foreign_keys = 1") 
cursor = conn.cursor()
# Create relational tables
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        shelf_location TEXT NOT NULL,
        added_by INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (category_id),
        FOREIGN KEY (added_by) REFERENCES users (user_id)
    );
    
    CREATE TABLE IF NOT EXISTS borrow_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (item_id) REFERENCES items (item_id)
    );
''')

# Sample Values 
cursor.execute('SELECT COUNT(*) FROM items')
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT OR IGNORE INTO users (username) VALUES ('Admin')")
    admin_id = cursor.execute("SELECT user_id FROM users WHERE username = 'Admin'").fetchone()[0]

    cursor.executemany('INSERT OR IGNORE INTO categories (category_name) VALUES (?)', 
                       [('Tool',), ('Electronic Component',)])
    
    sample_items = [
        ('Soldering Iron', 1, 5, 'A1', admin_id),
        ('Multimeter', 1, 3, 'A2', admin_id),
        ('10k Ohm Resistor', 2, 500, 'D3', admin_id),
        ('555 Timer IC', 2, 50, 'D3', admin_id),
        ('Wire Stripper', 1, 10, 'A2', admin_id),
        ('Arduino Uno', 2, 15, 'C1', admin_id)
    ]
    cursor.executemany('''
        INSERT INTO items (name, category_id, quantity, shelf_location, added_by)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_items)
    conn.commit()

# Define function if View All Items is selected
def print_items(records):
    print(f"\n{'-'*115}")
    print(f"{'ID':<4} | {'Item Name':<20} | {'Category':<20} | {'Qty':<4} | {'Shelf':<5} | {'Added By':<10} | {'Current Borrowers':<25}")
    print(f"{'-'*115}")
    if not records:
        print("No items found.")
    for row in records:
        # row[6] is the borrowers string. If it's None, we print "None"
        borrowers = row[6] if row[6] else "None"
        print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<20} | {row[3]:<4} | {row[4]:<5} | {row[5]:<10} | {borrowers:<25}")
    print(f"{'-'*115}\n")

# Startup page for users
print("\nWelcome to the Workshop Inventory System!")
current_username = input("Please enter your name to continue: ").strip()

cursor.execute("SELECT user_id FROM users WHERE username = ?", (current_username,))
user_result = cursor.fetchone()

if user_result:
    current_user_id = user_result[0]
    print(f"\nWelcome back, {current_username}!")
else:
    cursor.execute("INSERT INTO users (username) VALUES (?)", (current_username,))
    conn.commit()
    current_user_id = cursor.lastrowid
    print(f"\nNew user created! Welcome to the workshop, {current_username}!")

# Main Loop
while True:
    print(f"\n--- Main Menu ({current_username}) ---")
    print("1. View All Items")
    print("2. Add New Item")
    print("3. Borrow an Item")
    print("4. Return an Item")
    print("5. Delete an Item")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        cursor.execute('''
            SELECT 
                i.item_id, 
                i.name, 
                c.category_name, 
                i.quantity, 
                i.shelf_location, 
                u.username,
                (SELECT GROUP_CONCAT(users.username || ' (' || borrow_logs.quantity || ')') 
                 FROM borrow_logs 
                 JOIN users ON borrow_logs.user_id = users.user_id 
                 WHERE borrow_logs.item_id = i.item_id AND borrow_logs.return_date IS NULL) AS current_borrowers
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            JOIN users u ON i.added_by = u.user_id
        ''')
        print_items(cursor.fetchall())
        
    elif choice == '2':
        name = input("Enter item name: ")
        cursor.execute("SELECT * FROM categories")
        print("\nCategories:")
        for cat in cursor.fetchall():
            print(f"[{cat[0]}] {cat[1]}")
        try:
            cat_id = int(input("Enter Category ID: "))
            qty = int(input("Enter quantity: "))
            shelf = input("Enter shelf location (e.g., D3): ")
            cursor.execute('''
                INSERT INTO items (name, category_id, quantity, shelf_location, added_by) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, cat_id, qty, shelf, current_user_id))
            conn.commit()
            print(f"** '{name}' added to inventory by {current_username}! **")
        except ValueError:
            print("** Error: Category ID and Quantity must be numbers. **")
            
    elif choice == '3':
        try:
            item_id = int(input("Enter the ID of the item you want to borrow: "))
            borrow_qty = int(input("How many are you borrowing? "))
            cursor.execute("SELECT name, quantity FROM items WHERE item_id = ?", (item_id,))
            item = cursor.fetchone()
            
            if item and item[1] >= borrow_qty:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    INSERT INTO borrow_logs (user_id, item_id, quantity, borrow_date)
                    VALUES (?, ?, ?, ?)
                ''', (current_user_id, item_id, borrow_qty, timestamp))
                cursor.execute("UPDATE items SET quantity = quantity - ? WHERE item_id = ?", (borrow_qty, item_id))
                conn.commit()
                print(f"** Successfully borrowed {borrow_qty}x {item[0]}. **")
            else:
                print("** Error: Not enough stock or item doesn't exist. **")
        except ValueError:
            print("** Error: IDs and quantities must be numbers. **")
            
    elif choice == '4':
        cursor.execute('''
            SELECT b.log_id, i.name, b.quantity, b.borrow_date 
            FROM borrow_logs b
            JOIN items i ON b.item_id = i.item_id
            WHERE b.user_id = ? AND b.return_date IS NULL
        ''', (current_user_id,))
        active_borrows = cursor.fetchall()
        
        if not active_borrows:
            print("\nYou do not have any items currently checked out.")
            continue
            
        print("\nYour Active Borrows:")
        for log in active_borrows:
            print(f"[Log ID: {log[0]}] {log[2]}x {log[1]} (Borrowed: {log[3]})")
            
        try:
            log_id = int(input("\nEnter the Log ID of the item you are returning: "))
            cursor.execute("SELECT item_id, quantity FROM borrow_logs WHERE log_id = ? AND user_id = ? AND return_date IS NULL", 
                           (log_id, current_user_id))
            log_entry = cursor.fetchone()
            
            if log_entry:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE borrow_logs SET return_date = ? WHERE log_id = ?", (timestamp, log_id))
                cursor.execute("UPDATE items SET quantity = quantity + ? WHERE item_id = ?", (log_entry[1], log_entry[0]))
                conn.commit()
                print(f"** Item returned successfully at {timestamp}. Stock updated. **")
            else:
                print("** Error: Invalid Log ID. **")
        except ValueError:
            print("** Error: Log ID must be a number. **")

    elif choice == '5':
        try:
            item_id = int(input("Enter the ID of the item to delete: "))
            cursor.execute("SELECT name FROM items WHERE item_id = ?", (item_id,))
            item = cursor.fetchone()
            
            if item:
                cursor.execute("DELETE FROM borrow_logs WHERE item_id = ?", (item_id,))
                cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
                conn.commit()
                print(f"** '{item[0]}' and its associated borrow history were successfully deleted. **")
            else:
                print("** Error: Item ID not found. **")
        except ValueError:
            print("** Error: ID must be a number. **")
            
    elif choice == '6':
        print("Logging out. Goodbye!")
        break
        
    else:
        print("** Invalid choice. **")

conn.close()