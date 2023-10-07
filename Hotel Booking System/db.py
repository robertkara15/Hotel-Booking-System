# imports the modules needed to performn database queries in the program
import sqlite3
from os.path import exists, dirname
from pathlib import Path


# Database class to store methods which will perform all queries from the database
class Database:
    db_file_path = Path('users.db')
    connection = None
    cursor = None

    # establish path to database
    def __init__(self):
        db_exists = self.existing_database_on_disk()
        self.connection = sqlite3.connect(self.db_file_path)
        self.cursor = self.connection.cursor()

        # check if database already exists in file directory
        if db_exists:
            print("found, using existing db")
        else:
            print("not found, creating new empty db")
            print("Creating new db at: " + dirname(__file__) + "users.db")
            self.connection = sqlite3.connect(self.db_file_path)
            self.cursor = self.connection.cursor()
            self.create_new_db()

    # close database method
    def __del__(self):
        self.connection.close()

    # method in case of existing database
    def existing_database_on_disk(self):
        return self.db_file_path.is_file() and exists(self.db_file_path)

    # method to create a new database in the event of one not found
    def create_new_db(self):
        # creates the separate database tables
        self.cursor.execute('''CREATE TABLE Users (Username TEXT, Password TEXT, Points INTEGER, Role TEXT, Forename TEXT, Surname TEXT, CompletedTasks INTEGER)''')
        self.cursor.execute('''CREATE TABLE Offers (Name TEXT)''')
        self.cursor.execute('''CREATE TABLE Buffet (Item TEXT)''')
        self.cursor.execute('''CREATE TABLE Tasks (Duty TEXT)''')
        self.cursor.execute('''CREATE TABLE Reviews (Review TEXT)''')
        self.connection.commit()

        # test data to give the database
        self.cursor.execute('''INSERT INTO Offers VALUES (?)''', ["July Holiday Special"])
        self.cursor.execute('''INSERT INTO Tasks VALUES (?)''', ["Housekeeping"])
        self.cursor.execute('''INSERT INTO Reviews VALUES (?)''', ["Very clean and cosy rooms. Very happy with my stay."])

        # buffet items initial data
        buffet_items = ["Toast", "Scrambled eggs", "Fried potatoes", "Bacon", "Sausages", "Ham", "Corned beef hash",
                        "Biscuits", "Muffins", "Bagels", "Scones", "Tap water", "Bottled water",
                        "Orange juice", "Apple juice", "Cranberry juice", "Tea", "Coffee"]
        for item in buffet_items:
            self.cursor.execute('''INSERT INTO Buffet VALUES (?)''', [item])
        self.connection.commit()

    # method to add a task to the database
    def add_completed_task_for_user(self, user):
        self.cursor.execute('''SELECT Username, CompletedTasks FROM Users WHERE Username=?''', [user])
        tasks_completed = self.cursor.fetchone()[1]
        tasks_completed = int(tasks_completed) + 1
        self.cursor.execute('''UPDATE Users SET CompletedTasks=? WHERE Username=?''', (tasks_completed,user))
        self.connection.commit()
        return

    # method to read the employee leaderboard
    def fetch_employee_leaderboard(self):
        # most tasks completed will be first in the list
        self.cursor.execute('''SELECT Username, CompletedTasks FROM Users WHERE Role=? ORDER BY CompletedTasks DESC''', ["employee"])
        employees = list(self.cursor.fetchall())
        formatted_employees = []
        for person, tasks_completed in employees:
            formatted_employees.append(person + " - " + str(tasks_completed) + " duties filled")
        return formatted_employees

    # method to add a buffet item to the database
    def add_buffet(self, item):
        self.cursor.execute('''INSERT INTO Buffet VALUES (?)''', [item])
        self.connection.commit()
        return

    # method to read the buffet list
    def fetch_buffet(self):
        self.cursor.execute('''SELECT * FROM Buffet''')
        items = list(self.cursor.fetchall())
        formatted_list = []
        for item in items:
            formatted_list.append(item[0])
        return formatted_list

    # method to add an offer to the database
    def add_offer(self, item):
        self.cursor.execute('''INSERT INTO Offers VALUES (?)''', [item])
        self.connection.commit()
        return

    # method to retrieve offers
    def fetch_offers(self):
        self.cursor.execute('''SELECT * FROM Offers''')
        items = list(self.cursor.fetchall())
        formatted_list = []
        for item in items:
            formatted_list.append(item[0])

        return formatted_list

    # method to add a review to the database
    def add_review(self, item):
        self.cursor.execute('''INSERT INTO Reviews VALUES (?)''', [item])
        self.connection.commit()
        return

    # method to retrieve reviews
    def fetch_reviews(self):
        self.cursor.execute('''SELECT * FROM Reviews''')
        items = list(self.cursor.fetchall())
        formatted_list = []
        for item in items:
            formatted_list.append(item[0])
        print(formatted_list)
        return formatted_list

    # method to add a duty to the database
    def add_duty(self, item):
        self.cursor.execute('''INSERT INTO Tasks VALUES (?)''', [item])
        self.connection.commit()
        return

    # method to retrieve duties
    def fetch_duties(self):
        self.cursor.execute('''SELECT * FROM Tasks''')
        items = list(self.cursor.fetchall())
        formatted_list = []
        for item in items:
            formatted_list.append(item[0])
        return formatted_list

    # method to retrieve number of offers
    def number_of_offers(self):
        self.cursor.execute('''SELECT * FROM Offers''')
        items = list(self.cursor.fetchall())
        return len(items)

    # method to retrieve information based on username
    def find_user_info_by_username(self, username):
        result = []
        self.cursor.execute('''SELECT Username, Forename, Surname, Points from Users''')
        users = list(self.cursor.fetchall())
        for user in users:
            found_username = user[0]
            found_forename = user[1]
            found_surname = user[2]
            found_points = user[3]
            if found_username == username:
                full_name = found_forename + " " + found_surname
                result.append(full_name)
                result.append(found_points)
                break
        return result

    # adds a user to the database
    def add_user(self, username, password, rewards_points, role, forename, surname):
        if self.connection is None:
            raise ValueError("No DB!")
        else:
            # add user info to db here
            if self.is_existing_user(username):
                raise ValueError("ERROR: Username already exists")
            else:
                self.cursor.execute('''INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?)''', (username, password, rewards_points, role, forename, surname, 0))
                self.connection.commit()
                print("Added to database: {0} (role: {1}) ({2} rewards points) (0 completed duties)".format(username, role, rewards_points))
                return "SUCCESS: Username added to database as role: {0}".format(role)

    # method to remove users from db
    def remove_user(self, username):
        if self.connection is None:
            raise ValueError("No DB!")
        else:
            # Remove user from db
            if not self.is_existing_user(username):
                raise ValueError("ERROR: Username does not exist")
            else:
                self.cursor.execute('''DELETE FROM Users WHERE Username=?''', [username])
                self.connection.commit()
                print("Removed from database: {0}".format(username))
                return "SUCCESS: Username removed from database"

    # checks if there is an existing user with the given credentials
    def is_existing_user(self, username):
        self.cursor.execute('''SELECT Username FROM Users WHERE Username=?''', [username])
        result = self.cursor.fetchone()
        if result:
            # user already exists
            return True
        else:
            # safe to continue
            return False

    # method to retrieve rewards points
    def get_reward_points_for_user(self, username):
        self.cursor.execute('''SELECT Username, Points FROM Users WHERE Username=?''', [username])
        result = self.cursor.fetchone()[1]
        return result

    # method to retrieve user role
    def get_role_for_user(self, username):
        self.cursor.execute('''SELECT Username, Role FROM Users WHERE Username=?''', [username])
        result = self.cursor.fetchone()[1]
        return result

    # method to set rewards points
    def set_reward_points_for_user(self, username, reward_points):
        self.cursor.execute('''UPDATE Users SET Points=? WHERE Username=?''', (reward_points,username))
        self.connection.commit()

    # method to check if the user is valid
    def authorised_user(self, username, password):
        self.cursor.execute('''SELECT Username, Password FROM Users WHERE Username=?''', [username])
        result = self.cursor.fetchone()[1]
        # prevented duplicates from being added earlier
        if result:
            return password == result
        return False
