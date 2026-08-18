print("**************************************************\nWelcome to CPE106L Student Tracker!")

# Current dictionary
studentDict = {
    "2024108925": {
        "name": "James William G. Ty",
        "finalGrade": 98,
        "skills": ["Python", "Git", "SQL"],   
        "section": ("CPE106L", "1")           
    }
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
    menuDecision = int(input("\nPlease select what to do:\n\n[1]View student information\n[2]Add student information\n[3]Edit student information\n[4]Delete student information\n[5]Exit\nEnter here: "))
    
    # Process user decision
    match menuDecision:
        # Prints student information
        case 1:
            studentNumber = input("Please enter the student number of the requested student: ")
            if studentNumber in studentDict:
                print(f"\nStudent Name: {studentDict[studentNumber]['name']}")
                print(f"Student Number: {studentNumber}")
                print(f"Numerical Grade: {studentDict[studentNumber]['finalGrade']}")
                print(f"Letter Grade: {convertFinal(studentDict[studentNumber]['finalGrade'])}")
                
                # Fetching from Tuple
                print(f"Course & Group: {studentDict[studentNumber]['section'][0]} - Group {studentDict[studentNumber]['section'][1]}")
                
                # Fetching and formatting List
                print(f"Skills: {', '.join(studentDict[studentNumber]['skills'])}")
            else:
                print("I'm sorry we couldn't find this person, please check again or add a new student.")
                
        # Asks user the necessary details to add a new student
        case 2:
            newStuNum = input("Please add the student number of the student you want to add: ")
            newName = input("Please add the name of the student you want to add: ")
            newFinalGrade = int(input("Please add the final grade of the student you want to add: "))
            
            # Handling Tuple input
            newGroup = input("Please add the group number of the student you want to add: ")
            newSectionTuple = ("CPE106L", newGroup) 
            
            # Handling List input (Expanded version)
            newSkillsRaw = input("Please add skills separated by commas (e.g. Python, C++, HTML): ")
            
            newSkillsList = []                              # 1. Create an empty list
            raw_skills_split = newSkillsRaw.split(",")      # 2. Split the string at the commas
            
            for skill in raw_skills_split:                  # 3. Loop through each word
                clean_skill = skill.strip()                 # 4. Remove accidental spaces
                newSkillsList.append(clean_skill)           # 5. Add the clean word to the list
            
            studentDict[newStuNum] = {
                "name": newName, 
                "finalGrade": newFinalGrade, 
                "skills": newSkillsList,
                "section": newSectionTuple
            }
            print("Student added successfully!")
            
        # Asks user which student number to edit and which info to edit
        case 3:
            editStuNum = input("Please enter the student number of the student you want to edit: ")
            if editStuNum in studentDict:
                print(f"\nEditing: {studentDict[editStuNum]['name']}")
                print("[1] Edit Name")
                print("[2] Edit Final Grade")
                print("[3] Edit Group")
                print("[4] Edit Skills")
                editDecision = int(input("What would you like to edit? Enter here: "))
                
                if editDecision == 1:
                    studentDict[editStuNum]["name"] = input("Enter the new name: ")
                    print("Student name updated successfully!")
                elif editDecision == 2:
                    studentDict[editStuNum]["finalGrade"] = int(input("Enter the new final grade: "))
                    print("Final grade updated successfully!")
                elif editDecision == 3:
                    newGroup = input("Enter the new group: ")
                    # Replacing the old tuple with a new one
                    studentDict[editStuNum]["section"] = ("CPE106L", newGroup)
                    print("Group updated successfully!")
                elif editDecision == 4:
                    newSkillsRaw = input("Enter the new skills separated by commas: ")
                    
                    updatedSkillsList = []
                    raw_skills_split = newSkillsRaw.split(",")
                    
                    for skill in raw_skills_split:
                        clean_skill = skill.strip()
                        updatedSkillsList.append(clean_skill)
                        
                    studentDict[editStuNum]["skills"] = updatedSkillsList
                    print("Skills updated successfully!")
                else:
                    print("Invalid, returning to main menu.")
            else:
                print("I'm sorry we couldn't find this person, please check again.")
                
        # Added a safety check to prevent program crashes if the number isn't found
        case 4:
            delStuNum = input("Please enter the student number of the student information you want to delete: ")
            if delStuNum in studentDict:
                del studentDict[delStuNum]
                print("Student deleted successfully!")
            else:
                print("Error: Student number not found.")
                
        case 5:
            print("Exiting...Thank you!")