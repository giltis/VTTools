# Module for the BNL image processing project
# Developed at the NSLS-II, Brookhaven National Laboratory
# Developed by Gabriel Iltis, Oct. 2013
"""
This module is designed to facilitate image arithmetic and logical operations
on image data sets.
"""

import numpy as np
import parser
from skxray.img_proc.mathops import (logical_sub, logical_nand, logical_nor)
from numpy import (logical_xor, logical_and, logical_or, logical_not, add,
                   subtract, multiply, divide)


def arithmetic(operation,
               x1,
               x2):
    """
    This function enables basic arithmetic for image processing and data
    analysis. The function is capable of applying the basic arithmetic
    operations (addition, subtraction, multiplication and division) to two
    data set arrays, two constants, or an array and a constant.

    Parameters
    ----------
    operation : string
        addition:
            The addition of EITHER two images or volume data sets,
            OR an image/data set and a value. This function is typically
            used for offset purposes, or basic recombination of several
            isolated materials or phases into a single segmented volume.
        subtraction:
            Enables the subtraction of EITHER one image or volume data
            set from another, OR reduction of all values in an image/data set
            by a set value. This function is typically used for offset
            purposes, or basic isolation of objects or materials/phases in a
            data set.
        multiplication:
            Enables the multiplication of input 1 (x1) by input 2 (x2). The
            inputs can be of any valid numpy data type (e.g. an image or
            volume data a fixed, constant, value). This function is typically
            used for offset purposes (rescaling), or for assigning values in
            the generation of a labelfield identifying objects or
            materials/phases in a data set.

        division:
            Enables the division of input 1 (x1, numerator) by input 2 (x2,
            denominator). The inputs can be of any valid numpy data type
            (e.g. an image or volume data a fixed, constant, value). Basic
            tests are included in the division function which test for,
            and ensure that division by zero does not occur. This function is
            typically used for offset purposes (rescaling, normalization).

    x1 : {ndarray, int, float}
        Specifies the first input data set, or constant, to be offset or
        manipulated

    x2 : {ndarray, int, float}
        Specifies the second data set, or constant, to be offset or manipulated



    Returns
    -------
    output : {ndarray, int, float}
        Returns the resulting array or constant to the designated variable

    Example
    -------
    result = mathops.arithmetic_basic(img_1, img_2, 'addition')
    """
    operation_dict = {'addition' : add,
                      'subtraction' : subtract,
                      'multiplication' : multiply,
                      'division' : divide
    }
    if operation == 'division':
        if type(x2) is np.ndarray:
            if 0 in x2:
                raise ValueError("This division operation will result in "
                                 "division by zero values. Please reevaluate "
                                 "denominator (x2).")
        else:
            if float(x2) == 0:
                raise ValueError("This division operation will result in "
                                 "division by a zero value. Please "
                                 "reevaluate the denominator constant"
                                 " (x2).")

    output = operation_dict[operation](x1, x2)
    return output


def arithmetic_expression(expression,
                          A,
                          B,
                          C=None,
                          D=None,
                          E=None,
                          F=None,
                          G=None,
                          H=None):
    """
    This function enables more complex arithmetic to be carried out on 2 or
    more (current limit is 8) arrays or constants. The arithmetic expression
    is defined by the user, as a string, and after assignment of inputs A
    through H the string is parsed into the appropriate python expression
    and executed.  Note that inputs C through H are optional and need only be
    defined when desired or required.


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

+-        In the event that bitwise operations are required the operators &,
        |, ^, ~ may also be used, though I'm struggling to come up with a
        scenario where this will be used.

        Order of operations and parenthesis are taken into account when
        evaluating the expression.

    A : {ndarray, int, float}
        Data set or constant to be offset or manipulated

    B : {ndarray, int, float}
        Data set or constant to be offset or manipulated

    C : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated

    D : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated

    E : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated

    F : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated

    G : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated

    H : {ndarray, int, float}, optional
        Data set or constant to be offset or manipulated


    Returns
    -------
    output : {ndarray, int, float}
        Returns the resulting array or value to the designated variable

    Example
    -------
    result = mathops.arithmetic_custom('(A+C)/(B+D)', img_1, img_2, 2, 4)
    """
    output = eval(parser.expr(expression).compile())
    return output


def logic(operation,
          x1,
          x2=None):
    """
    This function enables the computation of the basic logical operations
    oft used in image processing of two image or volume  data sets. This
    function can be used for data comparison, material isolation,
    noise removal, or mask application/generation.

    Parameters
    ----------
    operation : str
        options include:
            'and' -- 2 inputs
            'or' -- 2 inputs
            'not' -- 1 input
            'xor' -- 2 inputs
            'nand' -- 2 inputs
            'subtract' -- 2 inputs

    x1 : {ndarray, int, float, list, tuple}
        Specifies the first reference

    x2 : {ndarray, int, float, list, tuple}
        Specifies the second reference

    Returns
    -------
    output : {ndarray, bool}
        Returns the result of the logical operation, which can be an array,
        or a simple boolean result.

    Example
    -------
    result = mathops.logic_basic('and', img_1, img_2)
    """
    logic_dict = {'and' : logical_and,
                  'or' : logical_or,
                  'not' : logical_not,
                  'xor' : logical_xor,
                  'nand' : logical_nand,
                  'nor' : logical_nor,
                  'subtract' : logical_sub
                  }
    output = logic_dict[operation](x1,
                                   x2)
    return output

__all__ = (add, subtract, multiply, divide, logical_and, logical_or,
           logical_nor, logical_xor, logical_not, logical_sub, logical_nand)