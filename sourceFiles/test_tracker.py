import datetime
from ty_jamesWilliam_labActivity3 import Habit, Habitmanager

print("--- STARTING HABIT TRACKER DEMO ---")

# 1. Start the manager
manager = Habitmanager()

# 2. Add some habits
print("\n[*] Adding habits: 'Gym', 'Code', and 'Read'...")
manager.addHabit("Gym")
manager.addHabit("Code")
manager.addHabit("Read")

# 3. Simulate logging over a few days
print("[*] Simulating logs to build streaks...")

# Time travel variables
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
two_days_ago = today - datetime.timedelta(days=2)

# Log "Gym" just for today (Streak: 1)
manager.habits[0].update(today)

# Log "Code" for 3 days in a row (Streak: 3)
manager.habits[1].update(two_days_ago)
manager.habits[1].update(yesterday)
manager.habits[1].update(today)

# 4. Print the final dashboard exactly like your main menu does
print("\n" + "="*56)
print("FINAL DASHBOARD DEMO:")
print("="*56)

for habit in manager.habits:
    print(f"habit name: {habit.name}")
    
    streak_msg = f"streak: {habit.getStreak()}"
    if habit.getStreak() > 2: # Lowered to 2 just so we can see the message in the demo!
        streak_msg += " (Keep up the good work!)"
    print(streak_msg)
    
    if habit.completionDates:
        formatted_dates = [d.strftime("%m/%d/%Y") for d in habit.completionDates]
        print(f"dates logged: {', '.join(formatted_dates)}")
    else:
        print("dates logged: None")
        
    print("") 
print("="*56)