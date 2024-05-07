import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import app.crud as crud # fixes some circular import issue
from app.dependencies import ContextManager
from app import schemas

def save_layout_to_db(layout, plan):
    #Saves seats into the database
    with ContextManager() as db:
        db_plan = crud.create_plan(db, plan)
        for i,(x,y) in enumerate(layout):
            crud.create_seat(
                db, 
                schemas.SeatCreate(
                    name=str(i), x=x, y=y, plan_id=db_plan.id
                )
            )
        print(f"Created {db_plan.name} with id {db_plan.id} "
              f"containing {len(layout)} seats")

def save_layout_to_file(layout, plan, path):
    #Saves file containing position of desks to workspaces folder
    with open(path, "w") as f:
        f.write(f"{plan.name},{plan.path}\n")
        f.writelines(f"{x.hex()},{y.hex()}\n" for x,y in layout)


def create_layout(name, img_path, num_desks=5):
    #Allows user input of desk positions on provided floorplan
    #Calls method to save layout
    plt.imshow(mpimg.imread(img_path))
    plt.xlabel("Use left mouse button to add desks, right mouse button to remove")
    desks = np.array(plt.ginput(num_desks))
    if (len(desks) != num_desks):
        raise ValueError("Not enough desks chosen")
    plan = schemas.PlanCreate(name=name, path=img_path)
    return desks, plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", help="Path to desk layout",
                        type=Path)
    parser.add_argument("num_desks", help="Number of desks to be chosen",
                        type=int)
    parser.add_argument("-n", "--name", help="Name of layout", type=str)
    parser.add_argument("-o", "--output_path", help="Output path", type=str)
    args = parser.parse_args()
    name = args.name if args.name else args.img_path.stem
    desks, plan = create_layout(name, args.img_path, args.num_desks)
    if (args.output_path):
        save_layout_to_file(desks, plan, args.output_path)
    else:
        save_layout_to_db(desks, plan)

if __name__ == "__main__":
    main()