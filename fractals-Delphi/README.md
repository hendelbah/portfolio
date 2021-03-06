# Fractals

<picture>
 <img src="fractal_1.png" alt="Beautiful Julia set">
</picture>

This is an application for visualizing fractal sets,namely Mandelbrot
set and Julia set. It is written in Delphi using Embarcadero RAD studio.
Main code is stored inside ``Unit1.pas``.

**I guess you don't have RAD studio to compile this code. So I hope you won't
mind running** ``Fractals.exe`` **I've already compiled, because actually it's cool.
There is hints on hover for each GUI element for better navigation.**

I won't explain here in detail what Mandelbrot and Julia sets are and what is
the math behind the calculations. If you're interested you can see it on wikipedia.
I just want to mention that this is all about complex numbers, so the fractal image
corresponds to the complex plain and every pixel refers to some complex number.

## How to use

The application draws the Mandelbrot set when you simply press the ``draw`` button.
If you used some feature below an nothing happened press this button again.

### Basic usage

<picture>
 <img src="fractal_2.png" alt="Mandelbrot set" width="49.5%">
</picture>
<picture>
 <img src="fractal_3.png" alt="4-th power of polynomial" width="49.5%">
</picture>

- You can specify number of max iterations that algorithm performs in the top left
  corner field. Bigger number makes the fractal more detailed but computation can
  take more time. This time is displayed in the bottom left colored rectangle.
- Also you can choose the power of polynomial function used in calculations in the
  droplist next to iterations field. It changes the fractal in some way, most noticeable
  are changes in its symmetry. It also affects the time of computation.
- You can zoom in and out with mouse scroll. If you zoom in, the detalization drops,
  so you might need to set higher iterations number.
- ``reset`` button resets zoom and adjusts window size if you've changed it
- When zoomed, you can move the image with ``ctrl+drag``.
- You can save current image in the app directory with ``Save image`` button

### Julia set drawing:

<picture>
 <img src="fractal_4.png" alt="Simple julia set">
</picture>

- Better you have set the droplist value (second GUI element from top row) to ``2``
- There is particular section in GUI for it: 4 long ``edit`` fields, 2 buttons with
  arrows right to them and a ``checkbutton`` after. Actually there is a set of Julia
  sets thus each of these sets uses some source complex number.
- You can enter the source number manually, there are these enter fields for, 1st
  and 2nd for real and imagine part in cartesian coordinates, 3d and 4th for r and ??
  in polar coordinates respectively. Pressing button with arrow translates either
  entered cartesian into polar coordinates or vice versa.
- You can simply pick the source number from current Mandelbrot set image using
  ``right mousebutton`` (remember, such image corresponds to complex plain).
- If source number is specified, check the ``checkbutton`` and press ``draw`` - voila.
- The resulting Julia set is something similar to surroundings of a point that you
  picked on the Mandelbrot set, so i recommend you to pick points near the black regions.

### GIF generation - the coolest thing:

<picture>
 <img src="fractal_1.gif" alt="Julia manifold" width="49.5%">
</picture>
<picture>
 <img src="fractal_2.gif" alt="3-d power Julia manifold" width="49.5%">
</picture>

- It works properly only if you have set the droplist value to ``2``, also make sure
  zoom is reset and iterations number isn't to high (values 100-200 is the best)
- **Just click on the rainbow rectangle and behold**
- If frames begin to change smoothly computation is finished. In that case you can save
  this thing as GIF with ``Save GIF`` button

#### I hope you'll enjoy!

