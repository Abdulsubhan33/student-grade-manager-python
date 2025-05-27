filename = "grades.txt"
print("Welcome to the Student Grades Management System")
def addstudent():
    name = input("Enter student name: ")
    rollno = input("Enter roll number: ")  
    grade = input("Enter grade: ")

    try:
        with open(filename, 'r') as d:
            data = d.readlines()
        for line in data:
            if not line.strip():
                continue
            existing_name, existing_rollno, existing_grade = line.strip().split(",")
            if existing_rollno.strip() == rollno:
                print(f"Roll number  {existing_rollno} , already exists. Please enter a different roll number.")
                return  # Stop further processing

        with open(filename, "a") as f:
            f.write(f"{name},{rollno},{grade}\n")
            print("Student added successfully.")
    except IOError:
        print("File not found or created ....")

def viewstudent():
    try:
        print("Name , Roll Number , Grade")
        z=open(filename , "r")
        lines = z.readlines()
        for line in lines:
            print(line.strip().split(","))
        z.close()
        if not lines:
            print("No records found.")
    except IOError:
        print("No records found")
def search():
    rollnumber = input("Enter roll number to search: ").strip()
    found = False
    try:
        with open(filename, "r") as f:
            for line in f:
                if not line.strip():
                    continue  
                name, rollno, grade = line.strip().split(",")
                if rollno.strip() == str(rollnumber):
                    print(f" Found: Name: {name}, Roll Number: {rollno}, Grade: {grade}")
                    found = True
                    break
        if found == False:
            print("Record not found.")
    except FileNotFoundError:
        print("No records or file found.")

def delete():
    rollnumber = int(input("eneter roll number to delete: "))
    found = False
    try:
        with open(filename ,'r') as f :
            lines = f.readlines()
        with open(filename, 'w') as f:
            for line in lines:
                if not line.strip():
                    continue
                name, rollno, grade = line.strip().split(",")
                if rollno.strip() == str(rollnumber):
                    found = True
                    print(f" Record with roll number {rollnumber} deleted successfully.")
                    continue  # skip writing this line
                f.write(line)

        if not found:
            print("Record not found.")
    except IOError:
        print(" File not found or not created.")
def mainmenu():
    while True:
        print("\n Main Menu:")
        print("1.Add Student")
        print("2.View student")
        print("3.Search student")
        print("4.Delete student")
        print("5.Exit")
        choice = int(input("enete number to make your choice : "))
        if choice == 1:
            addstudent()
        elif choice == 2:
            viewstudent()
        elif choice == 3:
            search()
        elif choice == 4 :
            delete()
        elif choice== 5:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("invalid choice ...")
if __name__ == "__main__":
    mainmenu()           





