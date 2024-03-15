import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def savelayout(layout, filename):
    #Saves csv file containing position of desks to Workspaces folder
    np.savetxt(filename, layout, delimiter=",")


def createlayout(floorplan, layoutname, desk_no=5):
    #Allows user input of desk positions on provided floorplan
    #Calls method to save layout
    plt.imshow(mpimg.imread(floorplan))
    plt.xlabel("Use left mouse button to add desks, right mouse button to remove")
    desks = np.array(plt.ginput(desk_no))
    savelayout(desks, layoutname)


def main():
    createlayout("Workspaces/example-floorplan.jpg", "Workspaces/desklayout.csv")


main()