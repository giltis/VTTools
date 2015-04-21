# Module for the BNL image processing project
# Developed at the NSLS-II, Brookhaven National Laboratory
# Developed by Gabriel Iltis, Oct. 2013
"""
This module is designed to facilitate image arithmetic and logical operations
on image data sets.
"""

import numpy as np
import parser
from skxray.img_proc.mathops import *
import logging

logger = logging.getLogger(__name__)

__all__ = ["arithmetic", "logical", "arithmetic_expression"]


def arithmetic(operation, x1, x2, div_by_zero='raise', out=None):
    """Arithmetic for inputs x1 and x2. result = x1 {+ - / *} x2

    Wrapper around numpy functions `np.add`, `np.subtract`, `np.divide`,
    `np.multiply`. As such, much of this docstring is copied from numpydocs to
    preserve the information

    Parameters
    ----------
    operation : {"add", "subtract", "multiply", "divide"}
        add:
            The sum of `x1` and `x2`, element-wise.  Returns a scalar if
            both  `x1` and `x2` are scalars.
            Note: Equivalent to `x1` + `x2` in terms of array broadcasting.
        subtract:
            The difference of `x1` and `x2`, element-wise.  Returns a scalar if
            both  `x1` and `x2` are scalars.
            Note: Equivalent to ``x1 - x2`` in terms of array broadcasting.
        divide:
            The quotient `x1/x2`, element-wise. Returns a scalar if
            both  `x1` and `x2` are scalars.
            Notes:
             - Equivalent to `x1` / `x2` in terms of array-broadcasting.
             - Behavior on division by zero can be changed using `seterr`.
             - When both `x1` and `x2` are of an integer type, `divide` will
               return integers and throw away the fractional part. Moreover,
               division by zero always yields zero in integer arithmetic.
        multiply:
            The product of `x1` and `x2`, element-wise. Returns a scalar if
            both  `x1` and `x2` are scalars.
            Note: Equivalent to `x1` * `x2` in terms of array broadcasting.

    x1, x2 : array_like
        Can be floats or arrays

    div_by_zero : divide : {'ignore', 'warn', 'raise'}, optional
        Treatment for division by zero.

    out : array, optional
        Array into which the output is placed. Its type is preserved and it
        must be of the right shape to hold the output. See numpy doc.ufuncs.

    Returns
    -------
    output : array-like  # use underscores for variable names, hyphens in prose
        Returns the resulting array or constant to the designated variable

    Example
    -------
    >>> x1 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    >>> x2 = np.array([[2, 0, 2], [0, 2, 0], [2, 0, 2]])
    >>> arithmetic('add', x1, x2)
    array([[2, 1, 2],
           [1, 3, 1],
           [2, 1, 2]])
    >>> arithmetic('subtract', x1, x2)
    array([[-2,  1, -2],
           [ 1, -1,  1],
           [-2,  1, -2]])
    >>> arithmetic('multiply', x1, x2)
    array([[0, 0, 0],
           [0, 2, 0],
           [0, 0, 0]])
    >>> arithmetic('divide', x1, x2, div_by_zero='raise')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/edill/dev/python/VTTools/vttools/to_wrap/image_proc.py",
      line 109, in arithmetic
        return op(x1, x2, out)
    FloatingPointError: divide by zero encountered in divide
    >>> arithmetic('divide', x1, x2, div_by_zero='warn')
    /home/edill/dev/python/VTTools/vttools/to_wrap/image_proc.py:109:
    RuntimeWarning: divide by zero encountered in divide
      return op(x1, x2, out)
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]])
    >>> arithmetic('divide', x1, x2, div_by_zero='ignore')
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]])
    """
    # ensure that inputs are numpy arrays
    x1 = np.asarray(x1)
    x2 = np.asarray(x2)
    # use numpy built-in functionality to handle divide by zero problems
    np.seterr(divide=div_by_zero)
    # can use this one-liner instead of the mapping dictionary
    op = getattr(np, operation)
    return op(x1, x2, out)


def arithmetic_expression(expression, A, B,
                          C=None, D=None, E=None, F=None, G=None, H=None):
    """Custom expression evaluator for up to 8 inputs A-H

    Note that it would probably be a good idea (at some point!) to make use of
    the `Interpreter` object in lmfit.asteval as it appears to be a rather
    parsing tool. @danielballan can speak to this better than I can

    Parameters
    ----------
    expression : string
        Note that the syntax of the mathematical expression must conform to
        python syntax,
        eg.:
            using * for multiplication instead of x
            using ** for exponents instead of ^

        Arithmetic operators:
            + : addition (adds values on either side of the operator
            - : subtraction (subtracts values on either side of the operator
            * : multiplication (multiplies values on either side of the
                operator
            / : division (divides the left operand (numerator) by the right
                hand operand (denominator))
            % : modulus (divides the left operand (numerator) by the right
                hand operand (denominator) and returns the remainder)
            ** : exponent (left operand (base) is raised to the power of the
                 right operand (exponent))
            // : floor division (divides the left operand (numerator) by the
                 right hand operand (denominator), but returns the quotient
                 with any digits after the decimal point removed,
                 e.g. 9.0/2.0 = 4.0)

        Logical operations are also included and available so long as the:
            > : greater than
            < : less than
            == : exactly equals
            != : not equal
            >= : greater than or equal
            <= : less than or equal

        In the event that bitwise operations are required the operators &,
        |, ^, ~ may also be used, though I'm struggling to come up with a
        scenario where this will be used.

        Order of operations and parenthesis are taken into account when
        evaluating the expression.

    A, B : {ndarray, int, float}
        Data set or constant to be offset or manipulated

    C, D, E, F, G, H : {ndarray, int, float}, optional
        Optional input ports for data sets or constants to be offset or
        manipulated using complex, custom, expressions


    Returns
    -------
    output : {ndarray, int, float}
        Returns the resulting array or value to the designated variable

    Example
    -------
    >>> A = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    >>> B = np.array([[2, 0, 2], [0, 2, 0], [2, 0, 2]])
    >>> C = 4
    >>> D = 1.3
    >>> arithmetic_expression('(A+C)/(B+D)', A, B, C, D)
    array([[ 1.21212121,  3.84615385,  1.21212121],
           [ 3.84615385,  1.51515152,  3.84615385],
           [ 1.21212121,  3.84615385,  1.21212121]])
    """
    return eval(parser.expr(expression).compile())


def logical(operation, x1, x2=None, out=None):
    """Boolean logic for inputs x1 and x2

    Parameters
    ----------
    operation : {'and', 'or', 'not', 'xor', `nor`, 'nand', 'sub'}
        Binary operations:
            and: Compute the truth value of x1 AND x2 element-wise.
            or: Compute the truth value of x1 OR x2 element-wise.
            xor: Compute the truth value of x1 XOR x2, element-wise.
            nor: Compute truth value of NOT (x1 OR x2)) element wise.
            nand: Computes the truth value of NOT (x1 AND x2) element wise.
            sub: Compute truth value of x1 AND (NOT (x1 AND x2)) element
                 wise.
        Unary operations:
            not: Compute the truth value of NOT x element-wise.

    x1, x2 : array-like
        Input arrays. `x1` and `x2` must be of the same shape.
        Note that x2 is optional for Unary operations

    out : array_like
        An array to store the output. Must be the same shape as input arrays

    Returns
    -------
    output : array-like
        Boolean result with the same shape as `x1` and `x2` of the logical
        operation on corresponding elements of `x1` and `x2`.

    See Also
    --------
    - User guide section on "Image Operations" (`/doc/resource/user-guide/image.rst`)
    - numpy functions: `np.logical_and`, `np.logical_or` and `np.logical_not`,
                       `np.logical_xor`
    - skxray functions: `skxray.img_proc.mathops.logical_nand`,
                        `skxray.img_proc.mathops.logical_nor, and
                        `skxray.img_proc.mathops.logical_sub`

    Example
    -------
    >>> x1 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    >>> x2 = np.array([[2, 0, 2], [0, 2, 0], [2, 0, 2]])
    >>> logical('and', x1, x2)
    array([[False, False, False],
           [False,  True, False],
           [False, False, False]], dtype=bool)
    >>> logical('or', x1, x2)
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
    >>> logical('not', x1, x2)  # note that 'not' will ignore x2
    array([[1, 0, 1],
           [0, 0, 0],
           [1, 0, 1]])
    >>> logical('xor', x1, x2)
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
    >>> logical('xor', x1, x2)
    array([[ True,  True,  True],
           [ True, False,  True],
           [ True,  True,  True]], dtype=bool)
    >>> logical('nand', x1, x2)
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
    >>> logical('sub', x1, x2)
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    """
    # can use this one-liner instead of the mapping dictionary
    op = globals()["logical_" + operation]
    # special case the unary operations
    if operation in {'not'}:
        return op(x1, out)
    else:
        return op(x1, x2, out)
