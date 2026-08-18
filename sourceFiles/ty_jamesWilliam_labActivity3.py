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
    def update(self,log_time=None): # logs
        if log_time is None:
            current_time = datetime.datetime.now()
        else:
            current_time = log_time

        if self.lastLog and self.lastLog.date() == current_time.date():
            # Return False to let the manager know the log was rejected
            return False 
            

        if self.lastLog:
            days_diff = (current_time.date() - self.lastLog.date()).days
            if days_diff == 1:
                self.streak += 1
            elif days_diff > 1:
                self.streak = 1
        else:
            self.streak = 1

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
manager = Habitmanager()
choice = 0
while choice != 4:
    choice = int(input("Please select what you want to do: \n[1]Log habit\n[2]Manage habits\n[3]View Dashboard\n[4]Exit\nSelection: "))
    
    # Choice Selection
    match choice:
        case 1:
            if not manager.habits:
                print("You currently have no habits. Please go to 'Manage habits' to add a habit first.")
            else:
                print("Current Habits:\n ")
                for habit in manager.habits:
                    print(f"[{manager.habits.index(habit)}] {habit.name}")
                    
                habitSelector = int(input("Please select which habit you would like to log on: "))
                
                # Capture the True/False result from the update method
                log_successful = manager.habits[habitSelector].update()
                
                if log_successful:
                    print("Habit logged successfully!")
                else:
                    print("You have already logged this habit today. Come back tomorrow!")

        case 2:
            if not manager.habits:
                print("I'm afraid you currently have 0 habits, please add a habit:")
                newHabitName = input("New habit name: ")
                manager.addHabit(newHabitName)
            else:
                manageChoice = int(input("Please select what you want to do: \n[1]Add habit\n[2]Delete habit\n[3]Exit\nSelection: "))
                match manageChoice:
                    case 1:
                        newHabitName = input("New habit name: ")
                        manager.addHabit(newHabitName)
                        print("Habit added successfully!")
                    case 2:
                        print("Current Habits:\n ")
                        for habit in manager.habits:
                            print(f"[{manager.habits.index(habit)}] {habit.name}")
                        delSelector = int(input("Please select which habit you would like to delete: "))
                        manager.delHabit(delSelector)
                        print("Habit deleted successfully!")
                    case 3:
                        print("Going back to Main Menu...")
        case 3:
            # --- NEW DASHBOARD LOGIC ---
            print("\n" + "="*56)
            if not manager.habits:
                print("No habits tracked yet.")
            else:
                for habit in manager.habits:
                    # Print habit name
                    print(f"habit name: {habit.name}")
                    
                    # Print streak and check for motivational message
                    streak_msg = f"streak: {habit.getStreak()}"
                    if habit.getStreak() > 7:
                        streak_msg += " (Keep up the good work!)"
                    print(streak_msg)
                    
                    # Format dates as m/d/y separated by commas
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





            



        
        
            


