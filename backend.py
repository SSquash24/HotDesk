# Backend Server that communicates with Front end
# Urls:
#   /       - Home page         - REQUIRES LOGIN
#   /login  - Login page
#   /book   - Booking page      - REQUIRES LOGIN

# POST Urls:
#   /login      -FORM: Login details (currently just username)
#   /logout
#   /book       -FORM: Booking details (currently just date)



# Run server locally with flask --app backend run
# Make sure flask is installed! (easily done with pip)

from flask import *
from userDB import users_getUID, users_isValidUID, users_getUsername
from officeDB import office_getBooking, office_tryBook

from datetime import datetime


app = Flask(__name__)

# secret key used for encoding session data
app.secret_key = b'QMBaG%&0w;JGJa1*8[Qm_2BpGCW'


# PAGE URLS (get requests) ----------------------------------------------------------------


@app.route("/")
def mainPage():

    #validate login details. If invalid logout (will send to login page)
    uid = None
    if 'uid' in session:
        uid = session['uid']
    
    if not users_isValidUID(uid):
        return logoutPost(True)
    

    return render_template('index.html', booking= office_getBooking(uid), name = users_getUsername(uid))

@app.route("/login")
def loginPage():
    return render_template('login.html')


@app.route("/book/")
def bookPage():
    
    #validate login details. If invalid logout (will send to login page)
    uid = None
    if 'uid' in session:
        uid = session['uid']
    
    if not users_isValidUID(uid):
        return logoutPost(True)

    return render_template('booking.html', name = users_getUsername(uid))



# POST REQUESTS -----------------------------------------------------------


@app.post("/login")
def loginPost():
    uid = users_getUID([request.form['username']])
    if uid == -1:
        flash("Invalid login credentials. Please try again!")
        return redirect(url_for("loginPage"))

    session['uid'] = uid
    return redirect(url_for("mainPage"))


@app.post("/logout")
def logoutPost(forcedLogout=False):
    session.clear()
    if not forcedLogout:
        flash("Successfully logged out!")
    return redirect(url_for("loginPage"))

@app.post("/book")
def bookPost():

    #get UID
    uid = None
    if 'uid' in session:
        uid = session['uid']

    error = office_tryBook(uid,
                datetime.strptime(
                    request.form['date'],
                    '%Y-%m-%d').date()
    )
    if error == None:
        flash(f"Successfully booked for {request.form['date']}")
    else:
        flash(f"Error: {error}")

    return bookPage()