import Recreator as recreator
from tkinter import filedialog
from tkinter import *
import os
import easygui


def main():
    root = Tk()
    root.geometry("500x100")
    frame = Frame(root)
    frame.pack()

    runNewSimulationButton = Button(frame, text="Run new Simulation", fg="black", command=runNewSimulation)
    runNewSimulationButton.pack(side=TOP)

    recreateSimulationButton = Button(frame, text="Recreate a Simulation", fg="black", command=recreateSimulation)
    recreateSimulationButton.pack(side=BOTTOM)

    runNewSimulation()

    bottomframe = Frame(root)
    bottomframe.pack(side=TOP)
    root.mainloop()




def runNewSimulation():
    os.system("python playground.py")


def recreateSimulation():
    #filename = filedialog.askopenfilename(initialdir="/", title="Select file",
    #                                      filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
   # filename = filedialog.askopenfilename(initialdir="/GitHub/Squary-Shappy/logs", title="Select file",
    #                                      filetypes=(("xml files", "*.xml"), ("all files", "*.*")))

    data_file_path = easygui.fileopenbox()
    #data_file_path = "logs/DATE_14-11-2019___TIME_16-25-27.xml"
#    data_file_path = "logs/DATE_14-11-2019___TIME_16-47-48.xml"
   # recreator.readXML(data_file_path)
    os.system("python recreator.py "+data_file_path)

if __name__ == "__main__":
    # call the main function
    main()
