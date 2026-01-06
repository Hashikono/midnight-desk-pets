# midnight-desk-pets
Desktop pets with a murder mystery twist to it (●'◡'●)

#IMPORTANT
- This program only works on windows as of now
- Your computer must be in ENGLISH or weird things will happen 

#References
- This is merely a model of the edge detection stuff for the sprite's usable platforms and will be
translated into GDscript once everything is finalized

- WINDOW HELPER SECTION OUTPUT: [window name, z layer #, x1, y1, x4, y4] -> coordinates will be transcribed to be vector2()
    - z layer # : top layer will be 0 and bottom layer will be the greatest number
    - we only need two coordinates for the corners of the rectanglular window (see figure below)

- EDGE DETECTION SECTION OUTPUT: [x1, y1, x2, y2] -> length/4 = how many horiontal edges there are

 1️⃣---------------2️⃣
 |                  |
 |                  |
 |                  |
 3️⃣---------------4️⃣


# MODEL 1
 \- \- \- \- \-   -> 0 0 0 - -
 \- \- \- \- \-   -> 0 0 0 1 1
 \- \- \- \- \-   -> 0 0 0 1 1
 \- \- \- \- \-   -> - 1 1 1 1
 \- \- \- \- \-   -> - 1 1 1 1
SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(2,0)  (3,1)-(4,1) -> [[0,0,2,0], [3,1,4,1]]
- IF THE COORDINATE PAIRS EQUAL, DON'T APPEND IT TO edgeDetection


# MODEL 2
 \- \- \- \- \-   -> 1 1 1 - -
 \- \- \- \- \-   -> 1 0 0 0 0
 \- \- \- \- \-   -> 1 0 0 0 0
 \- \- \- \- \-   -> - 0 0 0 0
 \- \- \- \- \-   -> - 0 0 0 0
SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(2,0)  (1,1)-(4,1) -> [[0,0,2,0], [1,1,4,1]]
- THE TOP LAYERS OF EACH BLOCK IS THE ONLY LAYER THAT SHOULD BE CONSIDERED

# IMPORTANT: JSON OUTPUT FORMAT
- Don't worry about everything in the screen section
- window section deals wih window related information (directly retrieved from windows API)
- edges section deals with the horizontal lines for the borders
    - Testing: make sure the y direction when you do the +/- 1 thing to make the red border seen does not get out of bound (edge-1)

{
    "screen": {
        "vx": -1920,
        "vy": 0,
        "width": 3840,
        "height": 1080,
        "cell_size": 20,
        "cols": 192,
        "rows": 54
    },
    "windows": [
        ["Window name", z-layor, x1, y1, x4, y4],
        ["VS Code", 0, -1920, 0, 0, 1080]
    ],
    "edges": [
        [x1, y1, x2, y2],
        [6, 6, 35, 6],
    ]

}
