# importing the necessary modules and files to allow login
from tkinter import *
import tkinter as tk
import time
import db
import employee_interface as ui_employee
import guest_interface as ui_guest
import datetime

# main class which contains methods required for login
class LoginForm:
    # method to set up the first form shown to the user
    def setup_login_form(self):
        # making a main form
        form = Tk()
        # defining the inputs as string variables before they are referenced
        self.username_login = StringVar()
        self.password_login = StringVar()
        self.login_feedback = StringVar()
        self.login_feedback.set("")

        # headings for initial screen
        form.title("Seaview Manor Booking System")
        form.geometry("1000x500")
        form.configure(bg="#0C44EB")

        # extracting the current date and time to display to the user
        today = time.strftime("%A %d/%m/%y")

        # label to display current date (in the form day name/day date/month/year)
        current_lbl = Label(form, text=today, bg="#0C44EB", fg="white", font=("Arial", 20))
        current_lbl.place(x=700, y=0)

        # title heading
        title_lbl = Label(form, text="       Main menu       ", bg="#0C44EB", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(form, text="Welcome to Seaview Manor", bg="#0C44EB", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=50)

        # login heading
        login_lbl = Label(form, text="Enter your login details", bg="#0C44EB", fg="white", font=("Arial", 20))
        login_lbl.pack(pady=35)

        # userID heading
        UID_lbl = Label(form, text="UserID:", bg="#0C44EB", fg="white", font=("Arial", 20))
        UID_lbl.place(x=250, y=250)

        # password heading
        PASS_lbl = Label(form, text="Password:", bg="#0C44EB", fg="white", font=("Arial", 20))
        PASS_lbl.place(x=250, y=300)

        # feedback from system
        feedback_lbl = Label(form, textvariable=self.login_feedback, bg="#0C44EB", fg="white", font=("Arial", 20))
        feedback_lbl.place(x=160, y=350)

        # entries for userID and password
        UID_ent = Entry(form, textvariable=self.username_login, width=25, bg="#0C44EB", fg="white")
        UID_ent.place(x=385, y=250)
        pass_ent = Entry(form, textvariable=self.password_login, width=25, bg="#0C44EB", fg="white", show='*')
        pass_ent.place(x=385, y=300)

        # buttons
        new_btn = Button(form, text="Create new user", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                         command=self.show_add_new_user)
        new_btn.place(x=100, y=400)
        login_btn = Button(form, text="Login", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                           command=self.handle_login)
        login_btn.place(x=395, y=400)
        help_btn = Button(form, text="Press for help", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                          command=self.show_help)
        help_btn.place(x=690, y=400)
        return form

    # method for setting up the form to create a new user
    def setup_new_user_form(self):
        # defining inputs as string variables to be used later on
        new_user_form = tk.Toplevel(self.root)
        self.new_user = StringVar()
        self.new_password = StringVar()
        self.new_forename = StringVar()
        self.new_surname = StringVar()
        self.new_user_feedback = StringVar()
        self.new_user_feedback.set("")
        self.new_user_role = StringVar()
        self.new_user_role.set("guest")
        new_user_form.title("ADD USER")
        new_user_form.geometry("1000x500")
        new_user_form.configure(bg="#0C44EB")

        # title heading
        title_lbl = Label(new_user_form, text="       Add User       ", bg="#0C44EB", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(new_user_form, text="Sign Up", bg="#0C44EB", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=50)

        # userID heading
        UID_lbl = Label(new_user_form, text="User ID:", bg="#0C44EB", fg="white", font=("Arial", 20))
        UID_lbl.place(x=270, y=300)

        # password heading
        PASS_lbl = Label(new_user_form, text="Password:", bg="#0C44EB", fg="white", font=("Arial", 20))
        PASS_lbl.place(x=270, y=350)

        # forename heading
        FORENAME_lbl = Label(new_user_form, text="Forename:", bg="#0C44EB", fg="white", font=("Arial", 20))
        FORENAME_lbl.place(x=270, y=200)

        # surname heading
        SURNAME_lbl = Label(new_user_form, text="Surname:", bg="#0C44EB", fg="white", font=("Arial", 20))
        SURNAME_lbl.place(x=270, y=250)

        # radio button to select guest role
        role_btn_guest = Radiobutton(new_user_form, variable=self.new_user_role, command=self.role_selector,
                                     text="Guest Role", value="guest", bg="#80909E", fg="black", font=("Arial", 12), width=20)
        role_btn_guest.place(x=800, y=250)

        # radio button to select employee role
        role_btn_employee = Radiobutton(new_user_form, variable=self.new_user_role, command=self.role_selector,
                                    text="Employee Role", value="employee", bg="#80909E", fg="black", font=("Arial", 12), width=20)
        role_btn_employee.place(x=800, y=300)

        # logout button
        logout_btn = Button(new_user_form, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=250, y=430)

        # new user button
        new_btn = Button(new_user_form, text="Add", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                         command=self.add_user)
        new_btn.place(x=550, y=430)

        # feedback
        feedback_lbl = Label(new_user_form, textvariable=self.new_user_feedback, bg="#0C44EB", fg="white",
                             font=("Arial", 20))
        feedback_lbl.place(x=250, y=350)

        # entries for user information - take string variables from earlier as inputs
        UID_entry = Entry(new_user_form, textvariable=self.new_user, width=30, bg="#c3dcfa", fg="black")
        UID_entry.place(x=450, y=300)
        pass_entry = Entry(new_user_form, textvariable=self.new_password, width=30, bg="#c3dcfa", fg="black", show='*')
        pass_entry.place(x=450, y=350)
        forename_entry = Entry(new_user_form, textvariable=self.new_forename, width=30, bg="#c3dcfa", fg="black", show='')
        forename_entry.place(x=450, y=200)
        surname_entry = Entry(new_user_form, textvariable=self.new_surname, width=30, bg="#c3dcfa", fg="black", show='')
        surname_entry.place(x=450, y=250)

        return new_user_form

    # method to check role of user created
    def role_selector(self):
        print(self.new_user_role.get())

    # shows help information
    def setup_help_form(self):
        # defining string variables for the help information
        help_window = tk.Toplevel(self.root)
        help_window.geometry("1000x500")
        help_window.configure(bg="#D3C6B8")
        help_window.title("HELP PAGE")
        self.help_text1 = StringVar()
        self.help_text2 = StringVar()
        self.help_text3 = StringVar()
        self.help_text1.set("")
        self.help_text2.set("")
        self.help_text3.set("")

        # title heading
        title_lbl = Label(help_window, text="       Info       ", bg="#D3C6B8", fg="black", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(help_window, text="Help Info", bg="#D3C6B8", fg="black", font=("Arial", 40))
        main_lbl.pack(pady=10)

        # help buttons for various roles
        help_btn_login = Button(help_window, text="Login Help", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                                command=self.show_login_help)
        help_btn_guest = Button(help_window, text="Guest Help", width=30, height=2, bg="#80909E", fg="black",
                                font=("Arial", 12), command=self.show_guest_help)
        help_btn_employee = Button(help_window, text="Employee Help", width=30, height=2, bg="#80909E", fg="black",
                                font=("Arial", 12), command=self.show_employee_help)
        help_btn_login.place(x=100, y=70)
        help_btn_guest.place(x=400, y=70)
        help_btn_employee.place(x=700, y=70)

        # commands to place the string variables on the form when they are created
        help_label1 = Label(help_window, textvariable=self.help_text1, width=100, font=("bold", 10), bg="#D3C6B8")
        help_label2 = Label(help_window, textvariable=self.help_text2, width=100, font=("bold", 10), bg="#D3C6B8")
        help_label3 = Label(help_window, textvariable=self.help_text3, width=100, font=("bold", 10), bg="#D3C6B8")
        help_label1.place(x=160, y=140)
        help_label2.place(x=160, y=250)
        help_label3.place(x=160, y=380)

        return help_window

    # login help text
    def show_login_help(self):
        self.help_text1.set("Main menu:\n User ID:\n - This text bar is for entering your User ID\n - If you do not have a User ID use the “Create new user” button\n Password:\n - This text bar is used to enter your password for its corresponding User ID\n - If you do not have a password use the  “Create new user” button\n Create new user:\n - The “Create new user” button will lead you to a screen where you can make a new account for a new user")
        self.help_text2.set("Login:\n - Once you have entered the necessary information into the two text bars, you can press this button to log into the system\n - Make sure that the information entered is correct, the system will tell you if it is not")
        self.help_text3.set("")

    # guest help text
    def show_guest_help(self):
        self.help_text1.set("Guest menu:\nReviews\n - Add a review to a database of already existing reviews\n - Read reviews that have been added to the system\nBook a stay:\n - Allows you to go on to the booking stage of the system to reserve a night at Seaview Manor\n - If any discounts such as student discount are needed be sure to refer to an employee as they will use their system to verify this\nRewards points:\n - With great loyalty, comes great rewards!")
        self.help_text2.set("\n - As you reserve more nights your loyalty points will rise, which can be redeemed in the “Current offers” part of the system\n Current offers:\n - Here you can browse the available offers\n - You can also redeem rewards points for special rewards offers\n - Alternatively there are seasonal offers year-round\n Menu:\n - Use this to view a database of the food available in the Breakfast Buffet\n Your booked stays:\n - Your currently booked stays are shown here")
        self.help_text3.set("Log out:\n - Press to exit interface")

    # employee help text
    def show_employee_help(self):
        self.help_text1.set("Employee menu:\nEmployee leaderboard:\n - Depending on the amount of duties completed by adding tasks to the duty rota employees are awarded points\n - Every month there is a new “Employee of the month” who can earn special rewards, maybe this month it will be you!\nCreate an offer:\n - Shows the amount of active offers\n - Allows you to create new offers\nMenu mode:\n - View restaurant menu\n - Add menu items")
        self.help_text2.set("Search customer:\n - A tick-box mode with simple information on every customer\n - Has the ability to add student discount and alter information for a user with their request\nCreate an offer:\n - Shows the amount of active offers\n - Allows you to create new offers")
        self.help_text3.set("Duty rota:\n - Shows the current active duties and when they need to be completed\n - Click the button to record a completed duty\nMenu mode:\n - View restaurant menu\n - Add menu items\n - Remove menu items\nLog out:\n - Press to exit interface")

    # uses the input information to perform validation
    def handle_login(self):
        print("validating...")
        self.authenticate(self.username_login.get(), self.password_login.get())
        return

    # outputs the combined help information to the form
    def show_help(self):
        help_form = self.setup_help_form()
        help_form.mainloop()
        return

    # constructor method to create a login object
    def __init__(self):
        self.root = self.setup_login_form()
        self.db = db.Database()

    # method for moving to mainloop
    def mainloop(self):
        self.root.mainloop()

    # method to show the new user
    def show_add_new_user(self):
        self.new_user_window = self.setup_new_user_form()

    # is used to check which user has logged in and opens the corresponding form for them
    def show_authorised_interface(self, username):
        role = self.db.get_role_for_user(username)
        if role == "employee":
            self.sub_interface = ui_employee.EmployeeInterface(username, self.db)
        if role == "guest":
            self.sub_interface = ui_guest.GuestInterface(username, self.db)

    # actually creates the user in question and assigns their information to separate variables
    def add_user(self):
        username = self.new_user.get()
        password = self.new_password.get()
        forename = self.new_forename.get()
        surname = self.new_surname.get()
        role = self.new_user_role.get()
        rewards_points = 0
        if role == "guest":
            # Start guests off with 100 rewards points
            rewards_points = 100
        # print statement so the current state of the account can be seen
        print("Adding User: ({0}) as {1}".format(username, role))

        # credential input validation
        try:
            self.validate_credentials(username, password)
        except ValueError as error:
            formatted_error = "Bad inputs: Error was: {0}".format(error)
            print(formatted_error)
            self.new_user_feedback.set(formatted_error)
            return
        try:
            self.db.add_user(username, password, rewards_points, role, forename, surname)
        except ValueError as insert_error:
            formatted_error = "Error adding to DB: {0}".format(insert_error)
            print(formatted_error)
            self.new_user_feedback.set(formatted_error)
            return
        formatted_success = "Success!"
        print(formatted_success)
        self.new_user_feedback.set(formatted_success)

    # sets up validation for both username and password using the 2 next methods
    def validate_credentials(self, username, password):
        self.validate_username(username)
        self.validate_password(password)
    # username validation
    def validate_username(self, username):
        # initially defines error as none
        error = None
        # tests no username given
        if username is None or username == "":
            error = "No username given!"
        # checks if username is too short
        if not error and len(username) < 3:
            error = "Username too short, please use more than 3 characters"
        # checks for the presence of any symbols
        if not error and not username.isalnum():
            error = "Username contains symbols, please use numbers and letters only"
        # checks if username is too long
        if not error and len(username) > 12:
            error = "Username too long, please use < 12 characters"
        if error is not None:
            raise ValueError(error)
        return True

    # password validation
    def validate_password(self, password):
        error = None
        # tests no password given
        if password is None or password == "":
            error = "No password given!"
        # checks if password is too short
        if not error and len(password) < 8:
            error = "Password too short, please use more than 8 characters"
        # checks strength of password
        if not error and (password.isalpha() or password.isnumeric()):
            error = "Password is too simple, please use a strong alphanumeric password"
        # checks if password is too long
        if not error and len(password) > 20:
            error = "Password too long, please use < 20 characters"
        if error is not None:
            raise ValueError(error)
        return True

    # performs the validation using the given information
    def authenticate(self, username, password):
        try:
            self.validate_credentials(username, password)
        except ValueError as error:
            # outputs error(s) in question
            formatted_error = "Bad inputs: Error was: {0}".format(error)
            print(formatted_error)
            self.login_feedback.set(formatted_error)
            return
        # error for the username not existing in the database
        if not self.db.is_existing_user(username):
            self.login_feedback.set("User does not exist.")
            return
        # successful login state
        if self.db.authorised_user(username, password):
            print("Successful login from user: {0} (reward points: {1})".format(username, self.db.get_reward_points_for_user(username)))
            self.show_authorised_interface(username)
            return
        # unsuccessful login state
        else:
            print("Failed login attempt from user: {0}".format(username))
            self.login_feedback.set("Error: Incorrect credentials.")
            return

