Image Operations in VisTrails
-----------------------------

"arithmetic" VisTrails module
=============================
The VisTrails module `arithmetic` enables basic arithmetic for image processing
and data analysis. The function is capable of applying the basic arithmetic
operations (addition, subtraction, multiplication and division) to two data set
arrays, two constants, or an array and a constant.

**Addition.** The addition of EITHER two images or volume data sets, OR an
image/data set and a value. This function is typically used for offset purposes,
or basic recombination of several isolated materials or phases into a single
segmented volume.

**Subtraction.** Enables the subtraction of EITHER one image or volume data set
from another, OR reduction of all values in an image/data set by a set value.
This function is typically used for offset purposes, or basic isolation of
objects or materials/phases in a data set.

**Multiplication.** Enables the multiplication of input 1 (x1) by input 2 (x2).
The inputs can be of any valid numpy data type (e.g. an image or volume data a
fixed, constant, value). This function is typically used for offset purposes
(rescaling), or for assigning values in the generation of a labelfield identifying
objects or materials/phases in a data set.

**Division.** Enables the division of input 1 (x1, numerator) by input 2 (x2,
denominator). The inputs can be of any valid numpy data type (e.g. an image or
volume data a fixed, constant, value). Basic tests are included in the division
function which test for, and ensure that division by zero does not occur. This
function is typically used for offset purposes (rescaling, normalization).

"arithmetic_expression" VisTrails module
========================================
The VisTrails module `arithmetic_expression` enables the use of custom
expressions to evaluate up to 8 input variables, named A-H. This function
enables more complex arithmetic to be carried out on 2 or more (current limit
is 8) arrays or constants. The arithmetic expression is defined by the user, as
a string, and after assignment of inputs A through H the string is parsed into
the appropriate python expression and executed.  Note that inputs C through H
are optional and need only be defined when desired or required.

"logical" VisTrails module
==========================
The VisTrails module `logical` enables the computation of the basic logical
operations oft used in image processing of two image or volume  data sets. This
function can be used for data comparison, material isolation, noise removal,
or mask application/generation.
