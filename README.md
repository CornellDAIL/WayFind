# WayFind: modular behavioral research and data collection tool
Made by Arthur Wayne with guidance from PhD candidate Qi Yang, and Professor Saleh Kalantari. 

![alt text](https://github.com/CornellDAIL/WayFind/blob/main/images/sample.gif)

## Description
WayFind is an open-source research tool for tracking live indoor location and behavioral marker data. After a literature review, we discovered a lack of any existing accurate, low-cost options to achieve this task. GPS, Wifi, Bluetooth methods are not cost-effective nor feasible to use indoors within a multi-story builidng, in our case <a href ="https://goo.gl/maps/QW24xXuv98w6MHvm6">MVR</a>.

In field studies that DAIL conducted with WayFind, researchers ran WayFind on a Microsoft Surface tablet with a stylus. Participants were fitted with additional data-collecting equipment including an EEG headset, physical motion sensors, a GSR sensor, a GoPro, and a joystick to measure intra-navigation uncertainty.

WayFind was created with modularity in mind—it can be run on any platform or device, and researchers of any discipline can tailor it to their specific research needs.

## Setup
WayFind is being run on Python v. 3.9.12.

### 1. Dependencies
WayFind utilizes the following libraries and versions for its functionality:
- `tkinter` (v. 8.6)
- `pandas` (v. 1.3.5)
- `PIL` (v. 9.0.1)
- `functools` (legacy)
- `subprocess` (legacy)
- `time` (legacy)
- `datetime` (legacy)
- `logging` (legacy)

Please install them prior to start.

### 2. Start

Once you've installed run WayFind, open your command prompt and run

`python start.py`

or

`python3 start.py`

Depending on how your Python installation is set up.
  
### 3. Mode Selection

Upon start, the user will be prompted with the following menu.

<img src="https://github.com/CornellDAIL/WayFind/blob/main/images/modes.png" width=150px height=150px>

There are two currently supported modes of WayFind: Live Tracking and Validation. In either mode data is set to autosave every five seconds (default).

#### A. Live Tracking
- Intended usage: researchers follow study participants in live experiments tracking location and behavioral markers.
- Through the interface the user can:
  - Plot live user location
  - Ascend or descend floors
  - Track behavioral markers (explained below in "Modularity -> Markers")
  - Open an in-app survey
  - Undo/redo actions 
 
#### B. Validation
- Intended usage: researchers validate live data post-experiment via cross-referencing other data (e.g. GoPro footage) and confirming through WayFind.
- Through the interface the user can:
  - Plot live user location
  - Ascend or descend floors
  - Track behavioral markers (explained below in "Modularity -> Markers")
  - Undo/redo actions 
- The Validation interface differs only slightly from Live Tracking in that after any plot or behavioral marker is recorded, a pop-up asking for a time-stamp will appear.

## Modularity
The following section details how WayFind can be tailored to other experimental settings.

### Overview

There are four python files in the root directory:
1. `start.py`
2. `select_layout.py`
3. `wayfind.py`
4. `constants.py`

`start.py` and `select_layout.py` are meta-files that operate the pre-app menus. These menus enable the user to determine the appropriate mode and layout and communicate this information to `wayfind.py`. The core of the codebase is in `wayfind.py`. `constants.py` contains relative constant variables, denoted in all-caps, following pep-8 naming conventions. All GUI are based in `Tkinter`. is We will use Live Tracking mode as the basis for detailing modularity.

### Maps
The map, which takes up a majority of the main GUI, is a Tkiner Canvas object with a 7:5 (default) aspect ratio. The images supplied are of dimension of 12600 × 9000 which then are rescaled to 1050 x 816 (default). To change what map(s) are displayed, two changes need to be made. First, `.jpg` images of the maps must be placed into the `/images` directory. Second, within `constants.py`, the elements of the `IMG_FILES` list must be changed to match the name of the map image files. Keep in mind that order matters, and order is ascending in terms of floor number.

### Survey
A press of the "Survey" button opens a popup that is formatted in accordance with `survey.csv` which is found in `/presets`. There are two types of survey questions: `slider` and `textbox`. Sliders give the user the option to input a numerical value on a fixed scale (e.g. overall uncertainty during task). Textboxes allow for alphanumeric input (e.g. participant ID). 

To customize the survey questions asked to a user, `survey.csv` can be modified. The file contains three columns: `type`, `question`, and `range`. `type` takes in either `slider` or `textbox`. `question` refers to the text which will appear above the respective slider or textbox. `range` is only applicable when `type` is `slider`, and takes in an integer range e.g. "-80,80." Below is what the default survey layout appears as.

<img src="https://github.com/CornellDAIL/WayFind/blob/main/images/surveyexample.png" width=184px height=100px>

### Markers

[TO CONTINUE]

### Landmarks

### Buttons
Once Live Tracking mode is selected, the following menu will appear to let the user choose which buttons she would like to use.

<img src="https://github.com/CornellDAIL/WayFind/blob/main/images/buttons.png" width=300px height=50px>

As the GUI is Tkinter-based, adding to or editing the existing functionality of buttons requires editing code. Within `wayfind.py`, lines 80-135 define the button layout and function calls triggered upon a button press. All functions within the code are preceded with a comment that summarizes functionalities. New functions can be created can be or existing ones can be tailored to researchers' task-specific needs.

### Constants

## Accessing Recorded Data
