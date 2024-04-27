import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from app.dependencies import ContextManager
from app.routers.admin import reset_db, ADMIN_USER_SCHEMA
from app import crud

# resets database to empty (with admin login)
def savelayout(layout):
    #Saves csv file containing position of desks to Workspaces folder
    #np.savetxt(filename, layout, delimiter=",")
    with ContextManager() as db:
        reset_db(db=db)
        crud.create_user(db, ADMIN_USER_SCHEMA)
        for i in range(len(layout)):
            crud.create_seat(db, str(i), layout[i][0], layout[i][1], i)


def createlayout(floorplan, desk_no=5):
    #Allows user input of desk positions on provided floorplan
    #Calls method to save layout
    plt.imshow(mpimg.imread(floorplan))
    plt.xlabel("Use left mouse button to add desks, right mouse button to remove")
    desks = np.array(plt.ginput(desk_no))
    savelayout(desks)


def main():
    createlayout("Workspaces/example-floorplan.jpg")


main()