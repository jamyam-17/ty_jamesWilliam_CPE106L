import datetime
# Create classes
class Habit :
    def __init__(self,name):
        self.name = name
        self.streak = 0
        self.lastLog = None
        self.creationDate = datetime.datetime.now()
        self.completionDates = []
        self.isLoggedToday = False
    #Setter Methods
    def update(self,log_time=None):
        if log_time is None:
            current_time = datetime.datetime.now()
        else:
            current_time = log_time
        # Prevents logging in the same day
        if self.lastLog and self.lastLog.date() == current_time.date():
            # Return False to let the manager know the log was rejected
            return False 
            
        # Adds streak once logged, resets when a day is skipped
        if self.lastLog:
            days_diff = (current_time.date() - self.lastLog.date()).days
            if days_diff == 1:
                self.streak += 1
            elif days_diff > 1:
                self.streak = 1
        else:
            self.streak = 1
        # Updates other attributes
        self.lastLog = current_time
        self.completionDates.append(current_time)
        self.isLoggedToday = True
        return True

    #Getter Methods
    def getStreak(self):
        return self.streak
    def getLastLog(self):
        return self.lastLog

class Habitmanager:
    def __init__(self):
        self.habits = []
    def addHabit(self,name):
        new_Habit = Habit(name)
        self.habits.append(new_Habit)
    def delHabit(self,index):
        if 0 <= index < len(self.habits):
            removed_habit = self.habits.pop(index)
            return removed_habit.name
        return None

# Welcome interface
print("Welcome to Habit Tracker!")
# Instantiates a habit manager object
manager = Habitmanager()
choice = 0
while choice != 4:
    choice = int(input("Please select what you want to do: \n[1]Log habit\n[2]Manage habits\n[3]View Dashboard\n[4]Exit\nSelection: "))
    
    # Choice Selection
    # CASE1: user chooses to log habits
    match choice:
        case 1:
            if not manager.habits:
                print("You currently have no habits. Please go to 'Manage habits' to add a habit first.")
            else:
                print("Current Habits:\n ")
                for habit in manager.habits:
                    print(f"[{manager.habits.index(habit)}] {habit.name}")
                # Habit logging selector
                habitSelector = int(input("Please select which habit you would like to log on: "))
                log_successful = manager.habits[habitSelector].update()
                # Checks log successful to prevent logging on the same day
                if log_successful:
                    print("Habit logged successfully!")
                else:
                    print("You have already logged this habit today. Come back tomorrow!")

        
        # CASE2: User chooses to delete/add habits
        case 2:
            if not manager.habits:
                print("I'm afraid you currently have 0 habits, please add a habit:")
                newHabitName = input("New habit name: ")
                manager.addHabit(newHabitName)
            else:
                manageChoice = int(input("Please select what you want to do: \n[1]Add habit\n[2]Delete habit\n[3]Exit\nSelection: "))
                match manageChoice:
                    # Creates a new habit
                    case 1:
                        newHabitName = input("New habit name: ")
                        manager.addHabit(newHabitName)
                        print("Habit added successfully!")
                    # Delete a habit
                    case 2:
                        print("Current Habits:\n ")
                        for habit in manager.habits:
                            print(f"[{manager.habits.index(habit)}] {habit.name}")
                        delSelector = int(input("Please select which habit you would like to delete: "))
                        manager.delHabit(delSelector)
                        print("Habit deleted successfully!")
                    # Go back to Main Menu
                    case 3:
                        print("Going back to Main Menu...")

        # CASE3: User chooses to show dashboard
        case 3:
            print("\n" + "="*21 + "HABIT DASHBOARD" + "="*21)
            if not manager.habits:
                print("No habits tracked yet.")
            else:
                for habit in manager.habits:
                    print(f"habit name: {habit.name}")
                    streak_msg = f"streak: {habit.getStreak()}"
                    # Adds a motivational message if consistent for a week
                    if habit.getStreak() > 7:
                        streak_msg += " (Keep up the good work!)"
                    print(streak_msg)
                    # Shows all other dates logged
                    if habit.completionDates:
                        formatted_dates = [date_obj.strftime("%m/%d/%Y") for date_obj in habit.completionDates]
                        dates_string = ", ".join(formatted_dates)
                        print(f"dates logged: {dates_string}")
                    else:
                        print("dates logged: None")
                        
                    print("") 
            print("="*56)
        case 4:
            print("Exiting Habit Tracker")





            



        
        
            


