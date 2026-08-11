print("**************************************************\nWelcome to CPE106L Student Tracker!")
# Current library
studentDict = {
    "2024108925":{"name" : "James William G. Ty",
                  "finalGrade" : 98,
                  "group" : "1"}
}
# Create conversion for finalGrade
def convertFinal(grade):
    if grade >= 98:
        return "A"
    elif grade >= 95:
        return "A-"
    elif grade >= 91:
        return "B+"
    elif grade >= 88:
        return "B"
    elif grade >= 85:
        return "B-"
    elif grade >= 81:
        return "C+"
    elif grade >= 77:
        return "C"
    elif grade >= 73:
        return "D+"
    elif grade >= 70:
        return "D"
    else:
        return "F"
    
# Prompt user what to do
menuDecision = 0
while menuDecision != 5:
    menuDecision = int(input("Please select what to do:\n\n[1]View student information\n[2]Add student information\n[3]Edit student information\n[4]Delete student information\n[5]Exit\nEnter here: "))
    # Process user decision
    match menuDecision:
        # Prints student information
        case 1:
            studentNumber = input("Please enter the student number of the requested student: ")
            if studentNumber in studentDict:
                print(f"\nStudent Name: {studentDict[studentNumber]["name"]}\nStudent Number: {studentNumber}\nNumerical Grade: {studentDict[studentNumber]["finalGrade"]}\nLetter Grade: {convertFinal(studentDict[studentNumber]["finalGrade"])}\nGroup: {studentDict[studentNumber]["group"]} ")
            else:
                print("I'm sorry we couldn't find this person, please check again or add a new student.")
        # Asks user the necessary details to add a new student
        case 2:
            newStuNum = input("Please add the student number of the student you want to add: ")
            newName = input("Please add the name of the student you want to add: ")
            newFinalGrade = int(input("Please add the final grade of the student you want to add: "))
            newGroup = input("Please add the group of the student you want to add: ")
            studentDict[newStuNum] = {"name":newName, "finalGrade": newFinalGrade, "group":newGroup}
            print("Student added!")
        # Asks user which student number to edit and which info to edit
        case 3:
            editStuNum = input("Please enter the student number of the student you want to edit: ")
            if editStuNum in studentDict:
                print(f"\nEditing: {studentDict[editStuNum]["name"]}")
                print("[1] Edit Name")
                print("[2] Edit Final Grade")
                print("[3] Edit Group")
                editDecision = int(input("What would you like to edit? Enter here: "))
                
                if editDecision == 1:
                    studentDict[editStuNum]["name"] = input("Enter the new name: ")
                    print("Student name updated successfully!")
                elif editDecision == 2:
                    studentDict[editStuNum]["finalGrade"] = int(input("Enter the new final grade: "))
                    print("Final grade updated successfully!")
                elif editDecision == 3:
                    studentDict[editStuNum]["group"] = input("Enter the new group: ")
                    print("Group updated successfully!")
                else:
                    print("Invalid choice, returning to main menu.")
            else:
                print("I'm sorry we couldn't find this person, please check again.")
        case 4:
            delStuNum = input("Please enter the student number of the student information you want to delete: ")
            del studentDict[delStuNum]
        case 5:
            print("Exiting...Thank you!")

        


