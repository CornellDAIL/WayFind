from constants import *
import pandas as pd
import tkinter as tk
from subprocess import call
from functools import partial

class run_app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.btn_frame = tk.Frame(self)
        self.live_track = tk.Button(self.btn_frame, height = BTN_HEIGHT, width = BTN_WIDTH, 
            text="Live Tracking", command=self.livetrack_mode)
        self.validation = tk.Button(self.btn_frame, height = BTN_HEIGHT, width = BTN_WIDTH, 
            text="Validation", command=self.validation_mode)
        self.btn_frame.pack()
        self.live_track.pack(side = 'top', pady = (2*BTN_SPACING,BTN_SPACING), padx = (3*BTN_SPACING,3*BTN_SPACING))
        self.validation.pack(side = 'top', pady = (BTN_SPACING,2*BTN_SPACING), padx = (3*BTN_SPACING,3*BTN_SPACING))
    
    def open_file(self, filename):
        call(["python3", filename])

    def livetrack_mode(self):
        buttons = (["0"] * 6)
        df = pd.DataFrame({'Buttons' : buttons})
        df.to_csv('presets/buttons.csv') 
        self.open_file("select_layout.py")

    def validation_mode(self):
        buttons = (["0"] * 5)
        buttons.append("1")
        df = pd.DataFrame({'Buttons' : buttons})
        df.to_csv('presets/buttons.csv') 
        self.open_file("select_layout.py")

if __name__ == "__main__":
    app = run_app()
    app.title('Select mode')
    app.iconbitmap(r'images/dail.ico')
    app.eval('tk::PlaceWindow . center')
    app.mainloop()