import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from app.dependencies import ContextManager
from app import crud, schemas

# resets database to empty (with admin login)
def save_layout(layout, plan):
    #Saves csv file containing position of desks to Workspaces folder
    #np.savetxt(filename, layout, delimiter=",")
    with ContextManager() as db:
        db_plan = crud.create_plan(db, plan)
        for i,(x,y) in enumerate(layout):
            crud.create_seat(db, schemas.SeatCreate(
                                 name=str(i), x=x, y=y, plan_id=db_plan.id
                            ))


def create_layout(name, img_path, num_desks=5):
    #Allows user input of desk positions on provided floorplan
    #Calls method to save layout
    plt.imshow(mpimg.imread(img_path))
    plt.xlabel("Use left mouse button to add desks, right mouse button to remove")
    desks = np.array(plt.ginput(num_desks))
    if (len(desks) != num_desks):
        raise ValueError("Not enough desks chosen")
    plan = schemas.PlanCreate(name=name, path=img_path)
    save_layout(desks, plan)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", help="Path to desk layout",
                        type=Path)
    parser.add_argument("num_desks", help="Number of desks to be chosen",
                        type=int)
    parser.add_argument("-n", "--name", help="Name of layout", type=str)
    args = parser.parse_args()
    name = args.name if args.name else args.img_path.stem
    create_layout(name, args.img_path, args.num_desks)

if __name__ == "__main__":
    main()