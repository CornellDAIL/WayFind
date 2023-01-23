from tkinter import *
from constants import *
from subprocess import call
import pandas as pd

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         chk.select() # pre-populate checkboxes
         self.vars.append(var)
   
   def checkboxState(self):
      return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
   live_mode = ['Vertical Navigation', 'Markers', 'Start/End Marker', 'Survey','Undo/Redo']
   valid_mode = ['Vertical Navigation', 'Task and Sign Seen Buttons', 'Undo/Redo']
   validation_mode_on = True if BUTTONS[5] == "1" else False
   mode = valid_mode if validation_mode_on else live_mode
   app = Tk()
   app.title('Select desired button layout')
   btnToggle = Checkbar(app, mode)
   btnToggle.pack(side='top')
   btnToggle.config(relief=GROOVE, bd=2)
   def allcheckboxStates():
      if validation_mode_on:
         temp_buttons = list(btnToggle.checkboxState())
         buttons = ["0"] * 6
         buttons[0], buttons[5], buttons[4] =  \
            temp_buttons[0], temp_buttons[1], temp_buttons[2]
      else: # live_mode_on
         buttons = list(btnToggle.checkboxState())
         buttons.append("0")
      df = pd.DataFrame({'Buttons' : buttons})
      df.to_csv('presets/buttons.csv') 
      call(["python3", 'wayfind.py'])
   Button(app, text='Launch', command=allcheckboxStates).pack()
   app.eval('tk::PlaceWindow . center')
   app.mainloop()