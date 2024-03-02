#Office database, with functions:

#   office_getBooking(uid) - returns Desk
#       get desk uid has booked for today
#       If uid didn't book, return None

#   office_tryBook(uid, Day) - returns None or string
#       attempts to book user uid for a desk on given day
#       On success, returns None
#       On failure, returns error string



#   UID - integer (all valid UIDs will be positive)
#   Desk - string
#   Day - DateTime.date


# Code below is for testing purposes, will need to be modified!

from datetime import date

bookings_today = {0: "A7", 2: "B4"}

def office_getBooking(uid):
    return bookings_today.get(uid)

def office_tryBook(uid, Day: date):
    if Day > date.today():
        return None
    return "Cannot book into the past!"