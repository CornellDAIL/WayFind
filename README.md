# WayFind: modular behavioral research and data collection tool
Made by Arthur Wayne, Qi Yang, and Saleh Kalantari. 

![alt text](https://github.com/CornellDAIL/WayFind/blob/main/images/sample.gif)

## Description
WayFind was created a multi-modal research tool to track live indoor location and behavioral marker data given the lack of any existing accurate, low-cost options. GPS, Wifi, Bluetooth methods are not cost-effective nor feasible to use indoors within a multi-story builidng, in this case <a href ="https://goo.gl/maps/QW24xXuv98w6MHvm6">MVR</a>.

In field studies that DAIL conducted utilizing WayFind, researchers ran WayFind on a Microsoft Surface tablet with a stylus. Participants were fitted with additional data-collecting equipment including an EEG headset, physical motion sensors, a GSR sensor, a GoPro, and a joystick to measure intra-navigation uncertainty.

WayFind was created with modularity in mind—it can be run on any platform or device, and researchers of any discipline can tailor it to their specific research needs.

## Setup
WayFind is being run on Python v. 3.9.12.

### 1. Dependencies
WayFind utilizes the following libraries and versions for its functionality:
- tkinter (v. 8.6)
- pandas (v. 1.3.5)
- PIL (v. 9.0.1)
- functools (legacy)
- subprocess (legacy)
- time (legacy)
- datetime (legacy)
- logging (legacy)

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

There are two currently supported modes of WayFind:
1. Live Tracking - researchers follow study participants in live experiments tracking location and behavioral markers
2. Validation - researchers validate live data post-experiment via cross-reference (e.g. GoPro footage) and confirm via app

## Modularity
The following section details how WayFind can be tailored to other experimental settings.

### Buttons

### Maps

### Survey

### Markers

### Landmarks
