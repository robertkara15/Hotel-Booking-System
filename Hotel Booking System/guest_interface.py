# importing the necessary modules and files for the guest interface
import db
from tkinter import *
import tkinter as tk
import time
import available_rooms
import datetime


# inherits from tk.Toplevel class
class GuestInterface(tk.Toplevel):
    def __init__(self, logged_in_user, db):
        tk.Toplevel.__init__(self)
        # making an form for adding users (add on more references to db if new functionalities needed)
        self.logged_in_user = logged_in_user
        self.db = db
        self.rewards_points = db.get_reward_points_for_user(logged_in_user)
        self.feedback = StringVar()
        self.booking_handler = available_rooms.AvailableRooms()
        self.booked_stays = []
        self.offer_amount = StringVar()
        self.formatted_booked_stays = StringVar()
        self.offer_amount.set("No available offers")

        # setting up the guest form
        self.title("Seaview Manor")
        self.geometry("1000x500")
        self.configure(bg="#4B67EA")

        # extracting the current date and time to display to the user
        today = time.strftime("%A %d/%m/%y")
        current_lbl = Label(self, text=today, bg="#4B67EA", fg="white", font=("Arial", 20))
        current_lbl.place(x=700, y=0)

        # title heading
        title_lbl = Label(self, text="        Guest menu        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(self, text="Guest menu", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=50)

        # personalised welcome back greeting
        login_lbl = Label(self, text="Welcome back, {0}".format(self.logged_in_user), bg="#4B67EA", fg="white", font=("Arial", 25))
        login_lbl.pack(pady=50)

        # rewards points label
        rewards_lbl = Label(self, text="You have {0} rewards points".format(self.rewards_points), width=30, height=2, bg="#A98025",
                             fg="black", font=("Arial", 12))
        rewards_lbl.place(x=395, y=300)

        # booking buttons
        book_btn = Button(self, text="Book a stay", command=self.book_stay, width=30, height=2, bg="#80909E", fg="black", font=("Arial", 12))
        book_btn.place(x=100, y=300)

        # the offers buttons link to a new page with some seasonal offers
        offers_btn1 = Button(self, text="Current offers", width=30, height=2, bg="#396320", fg="black",
                             font=("Arial", 12), command=self.show_offers_mode)
        offers_btn1.place(x=395, y=370)
        offers_btn2 = Button(self, textvariable=self.offer_amount, width=30, height=2, bg="#396320",
                             fg="black", font=("Arial", 12))
        offers_btn2.place(x=395, y=400)

        # help button
        help_btn = Button(self, text="Press for help", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12), command=self.show_help)
        help_btn.place(x=690, y=400)

        # reviews
        review_btn = Button(self, command=self.show_review_mode, text="Reviews", width=30, height=2, bg="#350F23", fg="black", font=("Arial", 12))
        review_btn.place(x=100, y=200)

        # buffet
        menu_btn = Button(self, command=self.show_buffet_mode, text="Menu", width=30, height=2, bg="#1603E9", fg="black", font=("Arial", 12))
        menu_btn.place(x=690, y=200)

        # booked stays
        booked_btn = Button(self, command=self.setup_user_bookings_form, text="Your booked stays", width=30, height=2, bg="#1603E9", fg="black",
                            font=("Arial", 12))
        booked_btn.place(x=690, y=300)

        # logout
        logout_btn = Button(self, command=self.logout, text="Log out", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)
        return

    # method to destroy the form to log out
    def logout(self):
        self.destroy()

    # brings up the buffet menu form
    def show_buffet_mode(self):
        buffet_form = self.setup_buffet_mode()
        buffet_form.mainloop()
        return

    # sets up the buffet menu form
    def setup_buffet_mode(self):
        buffet_guest_form = tk.Toplevel(self)
        buffet_guest_form.geometry("1000x500")
        buffet_guest_form.configure(bg="#4B67EA")
        buffet_guest_form.title("Seaview Breakfast Buffet")
        self.menu_items = StringVar()
        self.read_food_menu()

        # label with information
        buffet_label = Label(buffet_guest_form, textvariable=self.menu_items, width=100, font=("bold", 15),bg="#4B67EA", fg="white")
        buffet_label.place(x=0, y=100)

        # title heading
        title_lbl = Label(buffet_guest_form, text="        Seaview Manor buffet menu        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(buffet_guest_form, text="Buffet Menu", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # logout button
        logout_btn = Button(buffet_guest_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)
        return buffet_guest_form

    # uses db to fetch items from the database and formats them line by line
    def read_food_menu(self):
        all_items = self.db.fetch_buffet()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1

        self.menu_items.set(formatted_items)
        return

    # brings up review mode
    def show_review_mode(self):
        review_form = self.setup_review_mode()
        review_form.mainloop()
        return

    # sets up the review mode form
    def setup_review_mode(self):
        review_guest_form = tk.Toplevel(self)
        review_guest_form.geometry("1000x500")
        review_guest_form.configure(bg="#4B67EA")
        review_guest_form.title("Reviews")
        self.reviews = StringVar()
        self.read_reviews()
        self.new_review = StringVar()
        self.new_review.set("")

        # title heading
        title_rev = Label(review_guest_form, text="        Reviews        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_rev.place(x=0, y=0)

        # main heading
        main_rev = Label(review_guest_form, text="Reviews", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_rev.pack(pady=30)

        # information labels
        review_guest_form_label = Label(review_guest_form, textvariable=self.reviews, width=100, font=("bold", 15),
                             bg="#4B67EA", fg="white")
        review_guest_form_label.place(x=0, y=150)
        add_review_label = Label(review_guest_form, text="Add your review:", bg="#4B67EA", fg="white",
                                 font=("Arial", 20))
        add_review_label.place(x=50, y=100)

        # entry bar to add a review
        new_review_input = Entry(review_guest_form, textvariable=self.new_review, width=50, bg="#c3dcfa", fg="black")
        new_review_input.place(x=240, y=100)

        # buttons
        add_review_button = Button(review_guest_form, command=self.add_review, text="Add", width=30, height=2, bg="#D3C6B8", fg="black", font=("Arial", 12), )
        add_review_button.place(x=750, y=100)
        logout_btn = Button(review_guest_form, command=review_guest_form.quit(), text="Back", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)
        return review_guest_form

# method to add the review to the database
    def add_review(self):
        print("in add_review")
        self.db.add_review(self.new_review.get())
        self.new_review.set("")
        self.read_reviews()
        return

# method to read reviews from the database
    def read_reviews(self):
        print("updating form")
        all_items = list(self.db.fetch_reviews())
        all_items.reverse()
        formatted_items = ""
        # displays only up to 5 recent reviews in reverse order (newest first)
        # if more reviews are needed change the index on the if loop to n + 1 where n is the number of reviews
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n\n"
            index = index + 1
            if index == 6:
                break
        self.reviews.set(formatted_items)
        return

    # carries the form over to mainloop
    def setup_user_bookings_form(self):
        user_bookings = self.user_bookings_form()
        user_bookings.mainloop()
        return

    # sets up form to view currently booked stays
    def user_bookings_form(self):
        user_bookings_form = tk.Toplevel(self)
        user_bookings_form.geometry("1000x500")
        user_bookings_form.configure(bg="#4B67EA")
        user_bookings_form.title("Current Booked Stays")

        self.booked_stays = []

#        if self.booked_stays != []:
#            self.formatted_booked_stays.set(" ,".join(self.booked_stays.get()))
#        else:
#            self.formatted_booked_stays.set("")

        # information labels
        booked_stays_label = Label(user_bookings_form, textvariable=self.formatted_booked_stays, bg="#4B67EA", fg="white",
                               font=("Arial", 20))
        booked_stays_label.place(x=400, y=200)

        booked_stays_label2 = Label(user_bookings_form, text="Your booked stays:", bg="#4B67EA", fg="white",
                               font=("Arial", 20))
        booked_stays_label2.place(x=200, y=200)

        # title heading
        title_lbl = Label(user_bookings_form, text="        Booked Stays        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(user_bookings_form, text="Bookings", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)
        logout_btn = Button(user_bookings_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)
        return user_bookings_form

    # starts booking process
    def book_stay(self):
        booking_form = self.setup_booking_form()
        booking_form.mainloop()
        return

    # begins set up of booking form
    def setup_booking_form(self):
        book_form = tk.Toplevel(self)
        book_form.geometry("1000x500")
        book_form.configure(bg="#4B67EA")
        book_form.title("Book a room")
        self.days_available = StringVar()
        self.receipt = StringVar()
        self.receipt.set("")
        self.format_days_available()
        self.days_booked = []
        for day in self.booking_handler.days_of_week:
            self.days_booked.append(IntVar())

        # defines week as an integer variable
        self.week = IntVar()
        self.week.set(1)

        # defines month as an integer variable (index of 11 for 12 months)
        self.month = IntVar()
        self.month.set(self.booking_handler.months[11])

        # selector widget to pick month
        month_picker = OptionMenu(book_form, self.month, *self.booking_handler.months)
        month_picker.place(x=180, y=85, height=20, width=200)

        # selector widget to pick week
        week_picker = OptionMenu(book_form, self.week, *[1,2,3,4])
        week_picker.place(x=180, y=115, height=20, width=200)

        # logout button
        logout_btn = Button(book_form, command=book_form.quit(), text="Back", width=30, height=2, bg="#80909E", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=180, y=450)

        # confirm booking button
        book_confirm_button = Button(book_form, text="Confirm Days", width=50, height=2, bg="#80909E", fg="black",
                                font=("Arial", 12), command=self.confirm_booking)
        book_confirm_button.place(x=450, y=450)

        # title heading
        title_lbl = Label(book_form, text="        Book a stay        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(book_form, text="Bookings", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=20)

        # day labels
        monday_label = Checkbutton(book_form, text="Monday", variable=self.days_booked[0]).place(x=180, y=150, height=20, width=200)
        tuesday_label = Checkbutton(book_form, text="Tuesday", variable=self.days_booked[1]).place(x=180, y=190, height=20, width=200)
        wednesday_label = Checkbutton(book_form, text="Wednesday", variable=self.days_booked[2]).place(x=180, y=230, height=20, width=200)
        thursday_label = Checkbutton(book_form, text="Thursday", variable=self.days_booked[3]).place(x=180, y=270, height=20, width=200)
        friday_label = Checkbutton(book_form, text="Friday", variable=self.days_booked[4]).place(x=180, y=310, height=20, width=200)
        saturday_label = Checkbutton(book_form, text="Saturday", variable=self.days_booked[5]).place(x=180, y=350, height=20, width=200)
        sunday_label = Checkbutton(book_form, text="Sunday", variable=self.days_booked[6]).place(x=180, y=390, height=20, width=200)

        # label to show available days
        availability_label = Label(book_form, textvariable=self.days_available, width=30, font=("bold", 15), bg="#4B67EA", fg="white")
        availability_label.place(x=475, y=150)
        return book_form

    # method to create the text variable for available rooms
    def format_days_available(self):
        text = "Available rooms:\n\n"
        index = 0
        for day in self.booking_handler.days_of_week:
            text = text + day + ": " + str(self.booking_handler.weekdays_available[index]) + " rooms available\n"
            index = index + 1
        self.days_available.set(text)
        return

    # method to finalise bookings made using the selectors
    def confirm_booking(self):
        self.booking_handler.book_multiple_rooms(self.days_booked)
        self.format_days_available()
        # for loop to count the number of days booked
        index = 0
        number_of_days_booked = 0
        for day in self.days_booked:
            if day.get() == 1:
                number_of_days_booked = number_of_days_booked + 1
#                self.booked_stays.set(self.booked_stays.get() + self.booking_handler.days_of_week[index])
                self.booked_stays.append(self.booking_handler.days_of_week[index])
            index = index + 1

        # combines the days booked and formats them
        self.formatted_booked_stays.set(", ".join(self.booked_stays))
#       self.formatted_booked_stays.set(" ,".join(self.booked_stays.get()))
#       print(self.formatted_booked_stays.get())

        # reciept management
        # the number of rooms booked
        amount = len(self.booked_stays)
        # each room is £50
        price = 50 * amount
        # gets rewards points value of the user
        rewards = self.rewards_points
        # calculates how many sets of 100 points the user has
        counter = rewards // 100
        # multiplier to perform discount
        multiplier = 0.99**counter
        # total pricee after discount
        total_price = multiplier*price
        # discount on its own
        discount = price - total_price
        # number of rewards points given to user
        rewards_added = amount*25
        # print(rewards_added)
        # print(amount)
        # total rewards points after adding the new points
        new_rewards = rewards_added + rewards
        # variable to get the current date
        today = time.strftime("%d/%m/%y")
        # updates the database with the new rewards points value
        self.db.set_reward_points_for_user(self.logged_in_user, new_rewards)

        # format for receipt
        receipt_info = ["————————————————————————————————————————————————————————",
                        "               ~~~~~~SEAVIEW MANOR~~~~~~",
                        "USER ID:                                 " + self.logged_in_user,
                        "DATE:                                    " + str(today),
                        "ROOMS BOOKED:                            " + str(amount),
                        "PRICE BEFORE DISCOUNT:                   " + str(round(price, 2)),
                        "DISCOUNT:                                " + str(round(discount, 2)),
                        "PRICE AFTER DISCOUNT:                    " + str(round(total_price, 2)),
                        "REWARDS POINTS BEFORE:                   " + str(rewards),
                        "REWARDS POINTS ADDED:                    " + str(rewards_added),
                        "REWARDS POINTS AFTER:                    " + str(new_rewards),
                        "————————————————————————————————————————————————————————"
                        ]


        # outputs receipt to a text file to be printed
        information = "\n".join(receipt_info)
        print(information)
        with open("receipts.txt", "a") as reciepts_file:
            reciepts_file.write(information)
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

    # carries the form over to mainloop
    def show_offers_mode(self):
        offers_form = self.setup_offers_mode()
        offers_form.mainloop()
        return

    # creates form for the offers interface
    def setup_offers_mode(self):
        offers_guest_form = tk.Toplevel(self)
        offers_guest_form.geometry("1000x500")
        offers_guest_form.configure(bg="#4B67EA")
        offers_guest_form.title("Seaview Manor Offers")

        # title heading
        title_lbl = Label(offers_guest_form, text="        Seaview Manor offers        ", bg="#4B67EA", fg="white", font=("Arial", 20))
        title_lbl.place(x=0, y=0)

        # main heading
        main_lbl = Label(offers_guest_form, text="Current offers", bg="#4B67EA", fg="white", font=("Arial", 40))
        main_lbl.pack(pady=30)

        # button to logout
        logout_btn = Button(offers_guest_form, command=self.logout, text="Back", width=30, height=2, bg="#4B67EA", fg="black",
                          font=("Arial", 12))
        logout_btn.place(x=100, y=400)

        # label to display offers
        self.offers_items = StringVar()
        self.read_offers_menu()
        offers_label = Label(offers_guest_form, textvariable=self.offers_items, width=100, font=("bold", 15),bg="#4B67EA", fg="white")
        offers_label.place(x=0, y=125)
        return offers_guest_form

    # format the offers from the database into text format
    def read_offers_menu(self):
        all_items = self.db.fetch_offers()
        formatted_items = ""
        index = 1
        for item in all_items:
            formatted_items = formatted_items + str(index) + ": " + str(item) + "\n"
            index = index + 1
        self.offers_items.set(formatted_items)
        return