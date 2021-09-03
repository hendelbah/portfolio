Wildfire simulation
===================
This is an application for wildfire simulation based on cellular automata

Features
--------
Application generates a GIF file representing fire spreading in the forest

You can specify some parameters of fire spread.

Can set the wind, so fire will be more likely to spread in some direction

Can choose a directory to save that gif

Also you can open a picture, like a real forest photo from satellite,
that will be a pattern for initial grid generation. More blueish pixels
will turn into "river" cells which don't burn

Concept
-------
The model is such, that there is a grid of cells that changes every frame.
Each cell can have 3 different states:

* ``dirt``
* ``tree``
* ``burning``
Initial grid consists of ``dirt`` cells with randomly generated ``trees``
and one initial ``fire``

'burning' cell has 5 substates which represent its progress from ignition to going out.
Each frame any ```burning`` cell can ignite adjacent ``tree`` with a certain chance,
that differs for substates. Also, each frame substate changes and after reaching
last value it goes out and turns into dirt.

Program is optimized in such a way that it process only burning cells each frame,
searches around these cells for any ``tree`` and also excludes non-``tree`` from this search

UI
--
There is a TkInter UI, that consists of:

* ``probability`` field:
    the probability of ``tree`` generation on initial grid
* ``fire power values`` field:
    five integers (from 0 to 100) that represent chance (in percents)
    of fire spreading, corresponding to each individual substate of ``burning`` cell
* ``Number of tics`` field:
    The final number of frames to proceed
* ``GIF scale`` field:
    Scale of final GIF (only integer) relatively to the grid size.
    Picture, on which 1 pixel represents 1 cell doesn't look pleasant))
* ``Grid height`` field:
    Specify grid height
* ``Grid width`` field:
    Specify grid width
* ``Wind course`` field:
    Direction of wind in degrees clockwise starting from north
* ``Wind power`` field:
    Real number, ``0`` - no wind, ``3`` - quite strong wind
* ``Input image``:
    Grid can be generated from image pattern. Enter the path, or open it
    manually with ``open`` button. In this case ``grid height`` and
    ``grid width`` will be neglected.
* ``Output directory``:
    Directory to save resulting GIF. Enter the path, or open it
    manually with ``set`` button. If not specified GIF will be saved
    in the script directory
* ``Select initial fire`` button:
    When button is pressed, initial grid will be generated, and scaled
    image of it will appear sideways. Click somewhere on this image to
    put initial fire there, then program will generate the GIF and save it.
    Note that GIF generation can take some time/