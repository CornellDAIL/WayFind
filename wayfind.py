from constants import *
import tkinter as tk
import tkinter.font as TkFont
from tkinter import Toplevel
from tkinter import messagebox
import pandas as pd
import time
import datetime
import logging
from PIL import ImageTk, Image
from functools import partial

class RunApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.survey_num = 0
		self.floor_index = 0
		self.point_index = 0
		self.point_count = 0
		self.action_count = 0
		self.marker_index = 0
		self.validation_mode_on = True if BUTTONS[5] == "1" else False
		self.imgs = []
		self.plots = []
		self.plots_cache = []
		self.loc_data = {
			"time" : [],
			"unix" : [],
			"floor" : [],
			"marker" : [],
			"validation" : [],
			"x" : [],
			"y" : [],
		}
		self.redo_cache = {
			"time" : [],
			"unix" : [],
			"floor" : [],
			"marker" : [],
			"validation" : [],
			"x" : [],
			"y" : [],
		}
		# Saves most recent absolute x position
		self.x_abs = -1 
		self.y_abs = -1
		# Task and Sign Marker Buttons for validation
		self.task_btn_list = []
		self.sign_btn_list = []
		self.task_btn_index = 0
		self.sign_btn_index = 0
		for index, _ in enumerate(range(TASK_LIST_LENGTH)):
			self.task_btn_list.append('Task{}_Start'.format(index))
			self.task_btn_list.append('Task{}_End'.format(index))
		for index, _ in enumerate(range(SIGN_LIST_LENGTH)):
			self.sign_btn_list.append('Sign{}_Start'.format(index))
			self.sign_btn_list.append('Sign{}_End'.format(index))
		# Map files
		for img in IMG_FILES:
		    self.imgs.append(ImageTk.PhotoImage(
		    	Image.open(r'images/'+img).resize((X,Y),Image.ANTIALIAS)))
		# Frames
		self.canvas_frame = tk.Frame(self)
		self.canvas_frame.grid(column = 0, row = 0)
		self.btn_frame = tk.Frame(self)
		self.btn_frame.grid(column = 2, row = 0)
		# Canvases
		self.canvas = tk.Canvas(self.canvas_frame, width=X, height=Y, 
			bd = 2, bg = 'white', cursor = CURSOR_TYPE)
		self.canvas.create_image(X/2, Y/2, anchor = tk.CENTER, image = self.imgs[0])
		self.canvas.bind('<Button-1>', self.plot)
		self.canvas.after(MS_AUTOSAVE, self.auto_save)
		self.canvas.pack()
		self.mytext = tk.Text(self,height=51, width = 26, state="disabled")
		self.mytext.grid(column=1, row=0)
		# Pop-up Message
		self.fnt = TkFont.Font(size = 70)
		self.msg_list = []
		self.msg_list.append(self.canvas.create_text(X/2, Y/2, text='', font = self.fnt))
		# Buttons
		if BUTTONS[0] == '1':
			# Vertical Navigation
			self.ascend_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Ascend", command=self.ascend)
			self.descend_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT,
				width = BTN_WIDTH, text="Descend", command=self.descend)
			self.ascend_btn.pack(side = 'top')
			self.descend_btn.pack(side = 'top', pady = (0,BTN_SPACING))
		if self.validation_mode_on:
			self.task_btn = tk.Button(self.btn_frame, height=4*BTN_HEIGHT, width=BTN_WIDTH,
				text=self.task_btn_list[self.task_btn_index],
				command=partial(self.rotate_marker_valid, 'task'))
			self.sign_btn = tk.Button(self.btn_frame, height=4*BTN_HEIGHT, width=BTN_WIDTH,
				text=self.sign_btn_list[self.sign_btn_index],
				command=partial(self.rotate_marker_valid, 'sign'))
			self.task_btn.pack(side='top')
			self.sign_btn.pack(side='top', pady = (0,BTN_SPACING))
		if BUTTONS[1] == '1':
			# Markers
			self.marker_btn = tk.Button(self.btn_frame, height = 4*BTN_HEIGHT, 
				width = BTN_WIDTH, text=MARKERS[self.marker_index].replace(' ','\n'),
				command=self.rotate_marker)
			self.prev_marker_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Prev. Marker", command=self.prev_marker)
			self.next_marker_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT,
				width = BTN_WIDTH, text="Next Marker", command=self.next_marker)
			self.marker_btn.pack(side = 'top')
			self.prev_marker_btn.pack(side = 'top')
			self.next_marker_btn.pack(side = 'top', pady = (0,BTN_SPACING))
		if BUTTONS[2] == '1':
			# Start/End Marker
			self.start_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Mark Start", 
					command=partial(self.add_marker,'Start'))
			self.end_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Mark End", 
					command=partial(self.add_marker,'End'))
			self.start_btn.pack(side = 'top')
			self.end_btn.pack(side = 'top')
		if BUTTONS[3] == '1':
			# Survey
			self.survey_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Survey", 
					command=partial(self.popup, 'general'))
			self.survey_btn.pack(side = 'top', pady = (0,BTN_SPACING))
		if BUTTONS[4] == '1':
			# Undo/Redo
			self.undo_btn = tk.Button(self.btn_frame, height = BTN_HEIGHT, 
				width = BTN_WIDTH, text="Undo", 
				command=partial(self.process_mistake,True))
			self.redo_btn = tk.Button(self.btn_frame, 
				height = BTN_HEIGHT, width = BTN_WIDTH, 
				text="Redo", command=partial(self.process_mistake,False))
			self.undo_btn.pack(side = 'top')
			self.redo_btn.pack(side = 'top')
		self.after(MSG_TIME,self.delete_btn_msg)
	
	# Displays button press as message on-screen
	def btn_msg(self, button):
		self.msg_list.append(self.canvas.create_text(X/2,Y/2,
                        text=button, font = self.fnt))
		module_logger.info(button)
		self.mytext.see('end')

	# Deletes any on-screen button messages
	def delete_btn_msg(self):
		if(len(self.msg_list) > 0):
			for i in self.msg_list:
				self.canvas.delete(i)
		self.after(MSG_TIME,self.delete_btn_msg)

	# Opens data entry popup
	def popup(self, survey_type):
		self.w = PopupWindow(self, survey_type)
		self.w.b["state"] = "normal"
		self.wait_window(self.w.top)
		inVal = ''
		try:
			inVal = str(self.w.value)
		except:
			inVal = 'none'
		return inVal

	# Ascend/go up a floor
	def ascend(self):
		self.floor_index += 1
		if self.floor_index == len(self.imgs):
			self.floor_index -= 1
			print("We can't go up higher!")
		else:
			self.clear_canvas()
			self.action_count = 0
			self.btn_msg('Ascend')

	# Descend/go down a floor
	def descend(self):
		self.floor_index -= 1
		if self.floor_index < 0:
			self.floor_index = 0
			print("We can't go down further!")
		else:
			self.clear_canvas()
			self.action_count = 0
			self.btn_msg('Descend')

	# Go to the preivous marker button
	def prev_marker(self):
		if (self.marker_index > 0):
			self.marker_index += -1
			self.marker_btn.config(text=str(MARKERS[self.marker_index]).replace(' ','\n'))
		else:
			print("Cannot go back. We're at the first button")

	# Go to the next marker button
	def next_marker(self):
		marker_btn_text = str(MARKERS[self.marker_index]).replace(' ','\n')
		if (self.marker_index < len(MARKERS)-1):
			self.marker_index += 1
		else:
			self.marker_index = 0
		marker_btn_text = str(MARKERS[self.marker_index]).replace(' ','\n')
		self.marker_btn.config(text=marker_btn_text)

	# Add marker and go to next marker
	def rotate_marker(self):
		self.add_marker(str(MARKERS[self.marker_index]))
		self.next_marker()

	# add marker and go to next marker
	def rotate_marker_valid(self, valid_btn):
		if valid_btn == 'task':
			marker = str(self.task_btn_list[self.task_btn_index])
			self.btn_msg(marker)
			if (self.task_btn_index < len(self.task_btn_list)):
				self.task_btn_index += 1
			else:
				self.task_btn_index = 0
			self.task_btn.config(text=marker)
		else:
			marker = str(self.sign_btn_list[self.sign_btn_index])
			self.btn_msg(marker)
			if (self.sign_btn_index < len(self.sign_btn_list)):
				self.sign_btn_index += 1
			else:
				self.sign_btn_index = 0
			self.sign_btn.config(text=marker)
		validation = self.popup('valid')
		self.store_validation(validation, marker)

	# Add Unique Row Markers to Data
	def store_validation(self, validation, marker):
		self.plots.append(self.canvas.create_oval(0, 0, 0, 0, fill=CYAN))
		self.action_counter(False)
		if len(self.loc_data["x"]) > 0:
			self.add_data(self.loc_data["x"][-1], self.loc_data["y"][-1], marker, validation)
		else:
			self.add_data(0, 0, marker, validation)

	# Plot a point on the canvas
	def plot(self,event):
		x, y = (event.x), (event.y)
		x += CURSOR_OFFSET
		y += CURSOR_OFFSET
		self.x_abs = x
		self.y_abs = y
		self.plots.append(self.canvas.create_oval(
			x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
		self.clear_redo()
		marker = "Point"
		if self.validation_mode_on:
			validation = self.popup('valid')
			self.store_validation(validation, marker)
		else:
			self.store_plot(x, y, 'Point')

	# Plots given list of landmarks (const)
	def plot_lmark(self):
		lmark = LANDMARKS
		for i in range(len(lmark)):
			x1,y1 = lmark.loc[i,'X']*X, lmark.loc[i,'Y']*Y
			if lmark.loc[i,'Floor'] == FLOOR_DICT[self.floor_index]:
				self.canvas.create_oval(
					x1-PLOT_SIZE, y1-PLOT_SIZE, x1+PLOT_SIZE, y1+PLOT_SIZE, fill=BROWN)

	# Maintains a Trailing Plot count of length PLOT_COUNT_MAX
	def action_counter(self, isPoint, is_undo = False):
		if isPoint:
			if is_undo:
				self.point_count -= 1
				self.point_index -= 1
				self.action_count -= 1
			else:
				self.point_index += 1
				self.point_count += 1
				self.action_count += 1
				if self.point_count >= PLOT_COUNT_MAX:
					self.canvas.delete(self.plots[self.point_index-PLOT_COUNT_MAX])
		else:
			if is_undo:
				self.action_count -= 1
			else:
				self.action_count += 1
		if self.action_count < 0:
			self.action_count = 0
			print('Error: action_count below 0.')

	# Takes in absolute plot values and stores them through add_data
	def store_plot(self, x, y, marker):
		self.action_counter(True)
		x_rel = round(x/X,5)
		y_rel = round(y/Y,5)
		print(marker+' plotted at: ('+str(x_rel)+', '+str(y_rel)+')')
		self.add_data(x_rel,y_rel,marker)

	# Undo or Redo the most recent plot or marker
	def process_mistake(self, is_undo):
		if is_undo: # Undo
			if self.action_count > 0:
				x_rel = round(self.loc_data["x"][-1]/X,5)
				y_rel = round(self.loc_data["y"][-1]/Y,5)
				if x_rel == 0 and y_rel == 0: # marker
					self.action_counter(False, True)
					self.btn_msg('Undo {}'.format(self.loc_data["marker"][-1]))
				else:
					self.action_counter(True, True) # point
					self.plots_cache.append(self.canvas.coords(self.plots[-1]))
					last_plot = self.plots.pop()
					self.canvas.delete(last_plot)
					if "Sign" in self.loc_data["marker"][-1] or "Task" in self.loc_data["marker"][-1]:
						self.btn_msg('Undo {}'.format(self.loc_data["marker"][-1]))
					else:
						self.btn_msg('Undo Plot')
				if len(self.loc_data["x"]) > 0:	
					self.x_abs = self.loc_data["x"][-1]*X
					self.y_abs = self.loc_data["y"][-1]*Y
				self.pop_data(True)
			else:
				print('Cannot undo. Nothing to undo.')
		else: # Redo
			if len(self.plots_cache) != 0 or len(self.redo_cache["marker"]) != 0:
				self.loc_data["time"].append(self.redo_cache["time"].pop())
				self.loc_data["unix"].append(self.redo_cache["unix"].pop())
				self.loc_data["floor"].append(self.redo_cache["floor"].pop())
				self.loc_data["x"].append(self.redo_cache["x"].pop())
				self.loc_data["y"].append(self.redo_cache["y"].pop())
				self.loc_data["marker"].append(self.redo_cache["marker"].pop())
				x_rel = round(self.loc_data["x"][-1]/X,5)
				y_rel = round(self.loc_data["y"][-1]/Y,5)
				if len(self.loc_data["x"]) > 0:	
					self.x_abs = self.loc_data["x"][-1]*X
					self.y_abs = self.loc_data["y"][-1]*Y
				if x_rel != 0 and y_rel != 0: # is point
					x1,y1,x2,y2 = self.plots_cache.pop()
					self.plots.append(self.canvas.create_oval(x1, y1, x2, y2, fill=RED))
					self.action_counter(True)
					print('Point replotted at: ('+str(x_rel)+', '+str(y_rel)+')')
					self.btn_msg('Redo Plot')
				else: # is marker
					self.action_counter(False)
					self.btn_msg('Redo {}'.format(self.loc_data["marker"][-1]))
			else:
				print('Cannot redo. Redo cache is empty.')
 
	# Clear the Redo Cache
	def clear_redo(self):
		self.plots_cache = []
		self.redo_cache["time"] = []
		self.redo_cache["unix"] = []
		self.redo_cache["floor"] = []
		self.redo_cache["x"] = []
		self.redo_cache["y"] = []
		self.redo_cache["marker"] = []

	# Clear the canvas of all points (only visual)
	def clear_canvas(self):
		self.canvas.delete('all')
		self.canvas.create_image(X/2,Y/2, image = self.imgs[self.floor_index])
		self.action_count = 0
		self.clear_redo()
		self.plot_lmark()

	# Add Unique Row Markers to Data
	def add_marker(self, marker):
		self.canvas.create_oval(0,0,0,0, fill=CYAN)
		self.action_counter(False, False)
		self.add_data(0,0, marker)
		print('Marker {} added.'.format(marker))
		self.btn_msg(marker)

	# Append Data to Python Lists for Later Concatenation in a pd.DataFrame
	def add_data(self, x_rel, y_rel, marker, validation = None):
		current_img = IMG_FILES[self.floor_index]
		self.loc_data["time"].append(datetime.datetime.now())
		self.loc_data["unix"].append(time.time())
		self.loc_data["floor"].append(current_img[:current_img.find('.')])
		self.loc_data["x"].append(x_rel)
		self.loc_data["y"].append(y_rel)
		self.loc_data["marker"].append(marker)	 
		self.loc_data["validation"].append(validation)	 	


	# Pop last element of data lists
	def pop_data(self, isMistake):
		if isMistake == False:
			self.loc_data["time"].pop()
			self.loc_data["unix"].pop()
			self.loc_data["floor"].pop()
			self.loc_data["x"].pop()
			self.loc_data["y"].pop()
			self.loc_data["marker"].pop()
			self.loc_data["validation"].pop()
		else:
			self.redo_cache["time"].append(self.loc_data["time"].pop())
			self.redo_cache["unix"].append(self.loc_data["unix"].pop())
			self.redo_cache["floor"].append(self.loc_data["floor"].pop())
			self.redo_cache["x"].append(self.loc_data["x"].pop())
			self.redo_cache["y"].append(self.loc_data["y"].pop())
			self.redo_cache["marker"].append(self.loc_data["marker"].pop())
			self.redo_cache["validation"].append(self.loc_data["validation"].pop())

	# Concatenate data and save to .csv
	def save_data(self):	
		filename = ''
		if len(self.loc_data["time"]) == 0:
			filename = 'empty.csv'
		else:
			filename = str(self.loc_data["time"][-1])
			filename = filename[:filename.find(' ')]+'.csv'
			if self.validation_mode_on:
				filename = "validation-"+filename
			else:
				filename = "livetrack-"+filename
		(pd.DataFrame(self.loc_data)).to_csv("saved_data/"+filename)	
		print('Data Saved as '+filename)

	# Autosave data after MINS_AUTOSAVE minutes/MS_AUTOSAVE milliseconds
	def auto_save(self):
		self.save_data()
		print('Data Saved. AutoSave checkpoint at '+str(S_AUTOSAVE)+' seconds reached.')
		self.canvas.after(MS_AUTOSAVE,self.auto_save)
	
class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
		# initialize parent
        logging.StreamHandler.__init__(self)
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert("end", msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")

class PopupWindow(object):
	def __init__(self, master, survey_type):
		top = self.top = Toplevel(master)
		x = app.winfo_x()
		y = app.winfo_y()
		top.geometry("+%d+%d" % (x + 550, y))
		self.popup_resp = []
		if survey_type == "valid":
			self.l = tk.Label(top, text="Please enter the timestamp.")
			self.l.pack(side = 'top', pady = (BTN_SPACING, BTN_SPACING)
				, padx = (BTN_SPACING, BTN_SPACING))
			self.e = tk.Entry(top)
			self.e.pack(side = 'top', pady = (0, BTN_SPACING)
				, padx = (BTN_SPACING, BTN_SPACING))
			self.popup_resp.append(self.e)
		else:
			for i, qtype in enumerate(SURVEY.iloc[:,0]):
				qtext = SURVEY.iloc[i,1]
				if qtype == "slider":
					qrange = list(map(int,SURVEY.iloc[i,2].split(",")))
					self.create_slider(top, qtext, qrange)
				elif qtype == "textbox":
					self.create_textbox(top, qtext)
				else:
					raise NameError('Invalid Survey Question Type for index {}'.format(i)) 
		self.b = tk.Button(top, text='Ok', command=partial(self.cleanup, survey_type))
		self.b.pack(side = 'top')

	def create_slider(self, top, qtext, qrange):
		# slider
		self.popup_resp.append(tk.DoubleVar())
		slider_label = tk.Label(
			top,
			text=qtext
		)
		slider_label.pack(side = 'top')
		slider = tk.Scale(
			top,
			from_=qrange[0],
			to=qrange[1],
			orient='horizontal',  # vertical
			variable=self.popup_resp[i],
			length = 300
		)
		slider.pack(
			side = 'top', 
			pady = (0,BTN_SPACING/2), 
			padx = (BTN_SPACING,BTN_SPACING)
		)
	
	def create_textbox(self, top, qtext):
		self.l = tk.Label(top, text=qtext)
		self.l.pack(side = 'top', pady = (BTN_SPACING/2,0))
		self.e = tk.Entry(top)
		self.e.pack(side = 'top', padx = (BTN_SPACING,BTN_SPACING))
		self.popup_resp.append(self.e)

	# Close window and save data
	def cleanup(self, survey_type):
		resp = []
		for i in self.popup_resp:
			resp.append(i.get())
		if survey_type == "valid":
			self.value = resp[0]
		else:
			df = SURVEY
			df['response'] = resp
			filename = "survey_resp_{}.csv".format(self.survey_num)
			df.to_csv("saved_data/"+filename)	
			print("Saved file as {}".format(filename))
		self.top.destroy()


# Defines action when window close is pressed
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? Data is autosaved"):
        app.destroy()

if __name__ == "__main__":
	app = RunApp()
	app.title('Wayfind: Real-World Wayfinding Tool')
	app.iconbitmap(r'images/dail.ico')
	app.protocol("WM_DELETE_WINDOW", on_closing)
	stderr_handler = logging.StreamHandler()
	module_logger = logging.getLogger(__name__)
	module_logger.addHandler(stderr_handler)
	guiHandler = MyHandlerText(app.mytext)
	module_logger.addHandler(guiHandler)
	module_logger.setLevel(logging.INFO)
	module_logger.info("Button Event Log:")    
	app.eval('tk::PlaceWindow . center')
	app.mainloop()