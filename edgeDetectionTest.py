# This is merely a model of the edge detection stuff for the sprite's usable platforms and will be
# translated into GDscript once everything is finalized

#Input from window_helper.exe (or whatever we're using)
#WINDOW HELPER OUT: [window name, z layer #, x1, y1, x4, y4] -> coordinates will be transcribed to be vector2()
#   - z layer # : top layer will be 0 and bottom layer will be the greatest number
#   - we only need two coordinates for the corners of the rectanglular window (see figure below)
#EDGE DETECTION OUT: [x1, y1, x2, y2] -> length/4 = how many horiontal edges there are

# 1️⃣---------------2️⃣
# |                  |
# |                  |
# |                  |
# 3️⃣---------------4️⃣

#placeholder for output retrieved from window_helper.exe
windowHelperOutput1 = [
    "window 1", 0, 
    0, 0, 
    2, 2, 
    "window 2", 1, 
    1, 1, 
    4, 4
]

windowHelperOutput2 = [
    "window 1", 1, 
    0, 0, 
    2, 2, 
    "window 2", 0, 
    1, 1, 
    4, 4
]

#switch to test
windowHelper = windowHelperOutput1

#edge detection ouput (coordinates will be appended)
edgeDetectionOutput = []

#MODEL 1
# - - - - -   -> 0 0 0 - -
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> - 1 1 1 1
# - - - - -   -> - 1 1 1 1
#SHOULD OUTPUT: (0,0)-(0,2)  (1,3)-(1,4)
#   - IF THE COORDINATE PAIRS EQUAL, DON'T APPEND IT TO edgeDetection

#MODEL 1
# - - - - -   -> 1 1 1 - -
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> - 0 0 0 0
# - - - - -   -> - 0 0 0 0
#SHOULD OUTPUT: (0,0)-(0,2)  (1,1)-(1,4)

#THE TOP LAYERS OF EACH BLOCK IS THE ONLY LAYER THAT SHOULD BE CONSIDERED

#IMPORTANT: JSON OUTPUT FORMAT
# [
#   ["Visual Studio Code", 0, 100, 50, 1500, 900],
#   ["Chrome", 1, 0, 0, 1920, 1080],
#   ["Desktop", 2, -1920, 0, 0, 1080]
# ]




#assuming
model = []
for block in len(window_helper)/6:



