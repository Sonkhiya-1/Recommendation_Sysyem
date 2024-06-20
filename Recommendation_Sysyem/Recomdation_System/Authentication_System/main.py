from db_factory import DBFactory
from user import User
from getpass import getpass

def register():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    role = input("Enter role (Admin, Chef, Employee): ")

    db = DBFactory()
    user_data = db.get_user_by_username(username)
    
    if user_data:
        db.close()
        print("User already exists!")
        return

    db.register_user(username, password, role)
    db.close()
    print("User registered successfully!")

def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    db = DBFactory()
    user_data = db.get_user_by_username(username)
    
    if not user_data:
        db.close()
        print("Invalid credentials")
        return
    
    user = User.from_db(user_data)
    if User.check_password(password, user.password_hash):
        db.close()
        print(f"Logged in successfully as {user.role}!")
        return
    
    db.close()
    print("Invalid credentials")

def main():
    while True:
        choice = input("Choose an option: [register, login, exit]: ")
        if choice == 'register':
            register()
        elif choice == 'login':
            login()
        elif choice == 'exit':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
