import os
import csv
filename = "grades.txt"
# Only write header if file is empty or doesn't exist
if not os.path.exists(filename) or os.stat(filename).st_size == 0:
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Roll Number", "Grade"])
print("Welcome to the Student Grades Management System")
def addstudent():
    name = input("Enter student name: ").strip()
    rollno = input("Enter roll number: ")  
    grade = input("Enter grade: ")
    if not name or not rollno or not grade:
        print("All fields are required. Please try again.")
        return
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
        print("\n {:<20} {:<15} {:<10}".format("Name", "Roll Number", "Grade"))
        print("-" * 50)
        found = False
        with open(filename, "r") as z:
            for line in z:
                if not line.strip():
                    continue
                name, rollno, grade = line.strip().split(",")
                print("{:<20} {:<15} {:<10}".format(name, rollno, grade))
                found = True
        if not found:
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
    rollnumber = input("enter roll number to delete: ").strip()
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
def login():
    Username = "admin"
    Pass= "1234"
    attempt = 3
    while attempt > 0 :
        print("\n------ Login ---")
        username = input("Enter username : ").strip()
        password = input("Enter password : ").strip()
        if username == Username and password == Pass:
             print(f"Login successfully as {username}")
             return "admin"
        else:
            attempt -= 1
            print(f"Invalid credentials. You have {attempt} attempts left.")
    print("Too many failed attempts. Exiting the program.")
    return None
def mainmenu(role):
    while True:
        print("\nMain Menu:")
        print("1. Add Student" if role == "admin" else "")
        print("2. View Students")
        print("3. Search Student")
        print("4. Delete Student" if role == "admin" else "")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1" and role == "admin":
            addstudent()
        elif choice == "2":
            viewstudent()
        elif choice == "3":
            search()
        elif choice == "4" and role == "admin":
            delete()
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice or access denied.")

if __name__ == "__main__":
    role = login()
    if role:
        mainmenu(role)





