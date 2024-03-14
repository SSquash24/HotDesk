# Backend API with FastAPI 
# (I removed all the frontend endpoints with API "equivalents" for demonstration)


from fastapi import FastAPI, Request, HTTPException
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from userDB import users_getUID, users_isValidUID, users_getUsername
from officeDB import office_getBooking, office_tryBook

from datetime import date, datetime

# secret key used for encoding session data
secret_key = b'QMBaG%&0w;JGJa1*8[Qm_2BpGCW'

middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key, https_only=True)
]

routes = [
    Mount('/static', app=StaticFiles(directory='static'), name="static"),
]

app = FastAPI(middleware=middleware, routes=routes)



def logout(session, forcedLogout = False):
    session.clear()
    if not forcedLogout:
        return "Successfully logged out!"
    return ""

# PAGE URLS (get requests) ----------------------------------------------------------------

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(req: Request):

    #validate login details. If invalid logout (will send to login page)
    uid = None
    if 'uid' in req.session:
        uid = req.session['uid']
    
    if not users_isValidUID(uid):
        logout(req.session, forcedLogout=True)
        return RedirectResponse("/login")
    

    return templates.TemplateResponse(request=req, name="index.html", context={"booking": office_getBooking(uid), "name": users_getUsername(uid)})

@app.get("/login")
async def loginPage(req: Request):
    if 'uid' in req.session:
        return RedirectResponse("/")
    return templates.TemplateResponse(request=req, name="login.html", context={})
    
@app.get("/book")
async def bookPage(req: Request):

    #validate login details. If invalid logout (will send to login page)
    uid = None
    if 'uid' in req.session:
        uid = req.session['uid']
    
    if not users_isValidUID(uid):
        logout(req.session, forcedLogout=True)
        return RedirectResponse("/login")

    return templates.TemplateResponse(request=req, name="booking.html", context={"name": users_getUsername(uid)})


# POST REQUESTS -----------------------------------------------------------



@app.post("/login")
def login(username: str, req: Request):
    uid = users_getUID([username])
    if uid == -1:
        raise HTTPException(status_code=404, detail="Invalid login credentials. Please try again!")
    req.session['uid'] = uid
    return 


@app.post("/logout")
def logout_endpoint(req: Request):
    return logout(req.session)

@app.post("/book")
def book(req: Request, booking_date: date):

    #get UID
    uid = None
    if 'uid' in req.session:
        uid = req.session['uid']

    error = office_tryBook(uid, booking_date)
    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}")
    return f"Successfully booked for {booking_date}"
