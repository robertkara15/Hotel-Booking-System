# importing the necessary modules and files for the employee interface
import db
from tkinter import *
import tkinter as tk
import time


# inherits from tk.Toplevel class
class EmployeeInterface(tk.Toplevel):
    def __init__(self, logged_in_user, db):
        tk.Toplevel.__init__(self)
        # making an form for employees
        self.title("Employee menu")
        self.geometry("1000x500")
        self.configure(bg="#3E544F")
        self.logged_in_user = logged_in_user
        self.db = db
        self.feedback = StringVar()
        self.feedback.set("Welcome back, {0}".format(self.logged_in_user))
        self.offer_amount = StringVar()
        self.set_offer_amount()

        # extracting the current date and time to display to the user
        today = time.strftime("%A %d/%m/%y")
        current_lbl = Label(self, text=today, bg="#3E544F", fg="white", font=("Arial", 20))
        current_lbl.place(x=700, y=0)

        # title heading
        title_lbl = Label(self, text="        Employee Menu        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(self, text="Employee mode", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=50)

        # button to search for a customer
        search_btn = Button(self, command=self.show_search, text="Search customer", width=30, height=2, bg="#A98025", fg="black",
                            font=("Arial", 12))
        search_btn.place(x=100, y=200)

        # logout button
        logout_btn = Button(self, command=self.logout, text="Log out", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)

        # the offers buttons link to a new page with some seasonal offers
        offers_btn1 = Button(self, text="Create an offer", width=30, height=2, bg="#396320", fg="black",
                             font=("Arial", 12), command=self.show_offer_form)
        offers_btn1.place(x=395, y=370)
        offers_btn2 = Button(self, textvariable=self.offer_amount, width=30, height=2, bg="#396320",
                             fg="black", font=("Arial", 12))
        offers_btn2.place(x=395, y=400)

        # button to access help form
        help_btn = Button(self, text="Press for help", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12), command=self.show_help)
        help_btn.place(x=690, y=400)

        # leaderboard button
        leaderboard_btn = Button(self, command=self.show_leaderboard, text="Employee leaderboard", width=30, height=2, bg="#350F23", fg="black",
                            font=("Arial", 12))
        leaderboard_btn.place(x=100, y=300)

        # menu button
        menu_btn = Button(self, text="Menu mode", command=self.show_buffet_mode, width=30, height=2, bg="#1603E9", fg="black", font=("Arial", 12))
        menu_btn.place(x=690, y=200)

        # duties button
        duty_btn = Button(self, command=self.show_duty_form, text="Duty rota", width=30, height=2, bg="#1603E9", fg="black", font=("Arial", 12))
        duty_btn.place(x=690, y=300)

        # feedback label
        feedback_lbl = Label(self, textvariable=self.feedback, bg="#3E544F", fg="white",
                             font=("Arial", 25))
        feedback_lbl.pack(pady=50)
        return

    # method to destroy the form to log out
    def logout(self):
        self.destroy()

    # method to display search form
    def show_search(self):
        search_form = self.setup_search_form()
        search_form.mainloop()
        return

    # method to create search form
    def setup_search_form(self):
        search_form = tk.Toplevel(self)
        search_form.geometry("1000x500")
        search_form.configure(bg="#3E544F")
        search_form.title("Guest Search")
        self.found_text = StringVar()
        self.found_text.set("")
        self.search_username = StringVar()

        # main heading
        main_lbl = Label(search_form, text="Search customer", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # title heading
        title_lbl = Label(search_form, text="        Search customer        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # userID label
        UID_label = Label(search_form, text="Enter UserID:", bg="#3E544F", fg="white", font=("Arial", 20))
        UID_label.place(x=450, y=250)

        # label to return information found
        search_form_label = Label(search_form, textvariable=self.found_text, width=100, font=("bold", 15),
                             bg="#D3C6B8")
        search_form_label.place(x=0, y=100)

        # button to begin search
        find_guest_btn = Button(search_form, command=self.find_guest, text="Search customer", width=30, height=2, bg="#A98025", fg="black",
                            font=("Arial", 12))
        find_guest_btn.place(x=150, y=250)

        # entry to search userID
        search_input = Entry(search_form, textvariable=self.search_username, width=30, bg="#3E544F", fg="black")
        search_input.place(x=600, y=250)

        # button to log out
        logout_btn = Button(search_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=150, y=400)
        return search_form

    # method to search database to find guest
    def find_guest(self):
        details = self.db.find_user_info_by_username(self.search_username.get())
        result = "user: " + details[0] + " found with " + str(details[1]) + " points"
        self.found_text.set(result)
        return

    # method to show the leaderboard form
    def show_leaderboard(self):
        leaderboard_form = self.setup_leaderboard_form()
        leaderboard_form.mainloop()
        return

    # method to create the leaderboard form
    def setup_leaderboard_form(self):
        leaderboard_form = tk.Toplevel(self)
        leaderboard_form.geometry("1000x500")
        leaderboard_form.configure(bg="#3E544F")
        leaderboard_form.title("Leaderboard")
        self.leaderboard_text = StringVar()
        self.update_leaderboard()

        # title heading
        title_lbl = Label(leaderboard_form, text="        Employee Leaderboard        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(leaderboard_form, text="Leaderboard", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # feedback label
        leaderboard_form_label = Label(leaderboard_form, textvariable=self.leaderboard_text, width=100, font=("bold", 15),
                             bg="#3E544F", fg="white")
        leaderboard_form_label.place(x=0, y=100)

        # logout button
        logout_btn = Button(leaderboard_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=150, y=400)
        return leaderboard_form

    # method to update the leaderboard in the database
    def update_leaderboard(self):
        all_items = self.db.fetch_employee_leaderboard()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1
        self.leaderboard_text.set(formatted_items)
        return

    # method to show the duty form
    def show_duty_form(self):
        duty_form = self.setup_duty_form()
        duty_form.mainloop()
        return

    # method to create the duty form
    def setup_duty_form(self):
        duty_form = tk.Toplevel(self)
        duty_form.geometry("1000x500")
        duty_form.configure(bg="#3E544F")
        duty_form.title("View and change duties")
        self.duties = StringVar()
        self.new_duty = StringVar()
        self.read_duties()

        # title heading
        title_lbl = Label(duty_form, text="        Duties        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(duty_form, text="Duty rota", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # small heading label
        add_duty_label = Label(duty_form, text="Add new duty:", bg="#3E544F", fg="white",
                               font=("Arial", 20))
        add_duty_label.place(x=50, y=100)

        # entry for new duties to be added
        new_duty_input = Entry(duty_form, textvariable=self.new_duty, width=30, bg="#c3dcfa", fg="black")
        new_duty_input.place(x=200, y=100)

        # label to show duties
        duty_label = Label(duty_form, textvariable=self.duties, width=100, font=("bold", 15),
                           bg="#3E544F", fg="white")
        duty_label.place(x=0, y=150)

        # buttons
        add_duty_button = Button(duty_form, text="Add", width=30, height=2, bg="#80909E", fg="black",
                                 font=("Arial", 12),
                                 command=self.add_duty)
        add_duty_button.place(x=500, y=100)
        mark_done_button = Button(duty_form, text="Mark Completed", width=30, height=2, bg="#80909E", fg="black",
                                 font=("Arial", 12),
                                 command=self.mark_done)
        mark_done_button.place(x=750, y=100)

        # logout button
        logout_btn = Button(duty_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=50, y=400)

    # method to add duty to database
    def add_duty(self):
        self.db.add_duty(self.new_duty.get())
        self.read_duties()
        return

    # method to add a completed task
    def mark_done(self):
        self.db.add_completed_task_for_user(self.logged_in_user)
        return

    # method to read duties from the database and format them
    def read_duties(self):
        all_items = self.db.fetch_duties()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1
        self.duties.set(formatted_items)
        return

    # method to set the amount of offers from db
    def set_offer_amount(self):
        number_of_offers = self.db.number_of_offers()
        self.offer_amount.set("There are " + str(number_of_offers) + " offer(s)")
        return

    # method to show the offer form
    def show_offer_form(self):
        offers_form = self.setup_offer_form()
        offers_form.mainloop()
        return

    # method to create the offer form
    def setup_offer_form(self):
        offers_employee_form = tk.Toplevel(self)
        offers_employee_form.geometry("1000x500")
        offers_employee_form.configure(bg="#3E544F")
        offers_employee_form.title("Change offers")
        # set string variables to be output
        self.offer_items = StringVar()
        self.read_offers()
        self.new_offer = StringVar()

        # title heading
        title_lbl = Label(offers_employee_form, text="        Change offers        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(offers_employee_form, text="Offers", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # label to add offers
        add_offer_label = Label(offers_employee_form, text="Add new offer:", bg="#3E544F", fg="white",
                               font=("Arial", 20))
        add_offer_label.place(x=50, y=120)

        # label to show offers
        offer_label = Label(offers_employee_form, textvariable=self.offer_items, width=100, font=("bold", 15),
                             bg="#3E544F", fg="white")
        offer_label.place(x=0, y=250)

        # input for offers
        new_offer_input = Entry(offers_employee_form, textvariable=self.new_offer, width=30, bg="#c3dcfa", fg="black")
        new_offer_input.place(x=300, y=120)

        # button to add items
        add_item_button = Button(offers_employee_form, text="Add", width=30, height=2, bg="#80909E", fg="black",
                                 font=("Arial", 12), command=self.add_offer_item)
        add_item_button.place(x=750, y=120)

        # button to logout
        logout_btn = Button(offers_employee_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=50, y=400)

    # method to add offer items to database
    def add_offer_item(self):
        self.db.add_offer(self.new_offer.get())
        self.read_offers()
        return

    # method to read offers from database
    def read_offers(self):
        all_items = self.db.fetch_offers()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1

        self.offer_items.set(formatted_items)
        return

    # method to show the buffet menu form
    def show_buffet_mode(self):
        buffet_form = self.setup_buffet_mode()
        buffet_form.mainloop()
        return

    # method to create the buffet menu form
    def setup_buffet_mode(self):
        buffet_employee_form = tk.Toplevel(self)
        buffet_employee_form.geometry("1000x500")
        buffet_employee_form.configure(bg="#3E544F")
        buffet_employee_form.title("Seaview Breakfast Buffet (edit)")
        self.menu_items = StringVar()
        self.new_item = StringVar()
        self.read_food_menu()

        # title heading
        title_lbl = Label(buffet_employee_form, text="        Buffet Menu        ", bg="#3E544F", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(buffet_employee_form, text="Buffet Menu", bg="#3E544F", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # small heading label
        add_item_label = Label(buffet_employee_form, text="Add menu item to buffet:", bg="#3E544F", fg="white", font=("Arial", 20))
        add_item_label.place(x=50, y=100)

        # entry to add a new item
        new_item_input = Entry(buffet_employee_form, textvariable=self.new_item, width=48, bg="#c3dcfa", fg="black")
        new_item_input.place(x=300, y=100)

        # label to show the menu items
        buffet_label = Label(buffet_employee_form, textvariable=self.menu_items, width=100, font=("bold", 15), bg="#3E544F", fg="white")
        buffet_label.place(x=0, y=130)

        # button to confirm add item
        add_item_button = Button(buffet_employee_form, text="Add", width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12),
                         command=self.add_food_menu)
        add_item_button.place(x=750, y=100)

        # button to logout
        logout_btn = Button(buffet_employee_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=50, y=400)
        return buffet_employee_form

    # method to add to the buffet menu
    def add_food_menu(self):
        self.db.add_buffet(self.new_item.get())
        self.read_food_menu()
        return

    # method to read the buffet menu items from db
    def read_food_menu(self):
        all_items = self.db.fetch_buffet()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1
        self.menu_items.set(formatted_items)
        return

    # outputs the combined help information to the form
    def show_help(self):
        help_form = self.setup_help_form()
        help_form.mainloop()
        return

    # shows help information
    def setup_help_form(self):
        # making an form for showing help
        help_window = tk.Toplevel(self)
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
        help_btn_login = Button(help_window, text="Login Help", width=30, height=2, bg="#80909E", fg="black",
                                font=("Arial", 12),
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
