# importing datetime to introduce the concept of dates to the code
import datetime

# creates the room concept in a separate class
class AvailableRooms:
    def __init__(self):
        # starts off with days, months, and week numbers
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        self.week_of_month = 1
        # amount of rooms available on each day of the week
        self.weekdays_available = [12, 14, 20, 15, 20, 18, 16]
        self.today = datetime.datetime.today().weekday()
        self.today_index = self.today - 1

    # method to book rooms multiple times
    def book_multiple_rooms(self, days_of_week):
        index = 0
        for day in days_of_week:
            if day.get() == 1:
                # booking selected
                self.book_room(index)
            index = index + 1

    # method to book rooms
    def book_room(self, day_of_week):
        current_rooms_open = self.weekdays_available[day_of_week]
        self.weekdays_available[day_of_week] = current_rooms_open - 1
        return



