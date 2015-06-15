# Module for the BNL image processing project
# Developed at the NSLS-II, Brookhaven National Laboratory
# Developed by Gabriel Iltis, Sept. 2014
"""
This module contains test functions for the file-IO functions
for reading and writing data sets using the netCDF file format.

The files read and written using this function are assumed to
conform to the format specified for x-ray computed microtomorgraphy
data collected at Argonne National Laboratory, Sector 13, GSECars.
"""

import numpy as np
import six
import vttools.to_wrap.image_proc as img
from numpy.testing import assert_equal, assert_raises, raises


@raises(AttributeError)
def arithmetic_helper_fails(op, x1, x2):
    img.arithmetic(op, x1, x2)


def test_arithmetic_fails():
    ops = ['addition', 'subtraction', 'division', 'multiplication']
    x1s = [0] * len(ops)
    x2s = [0] * len(ops)
    for op, x1, x2 in zip(ops, x1s, x2s):
        yield arithmetic_helper_fails, op, x1, x2


def test_arithmetic_basic():
    """
    Test function for the image processing function: arithmetic_basic

    """
    test_array_1 = np.zeros((30, 30, 30), dtype=np.int)
    test_array_1[0:15, 0:15, 0:15] = 1
    test_array_2 = np.zeros((30, 30, 30), dtype=np.int)
    test_array_2[15:29, 15:29, 15:29] = 87
    test_array_3 = np.ones((40, 30, 30), dtype='float')
    test_array_3[10:20, 10:20, 10:20] = 87.4
    test_array_4 = np.zeros((30, 30), dtype=np.int)
    test_array_4[24:29, 24:29] = 254

    test_1D_array_1 = np.zeros(100, dtype=np.int)
    test_1D_array_1[0:30] = 50
    test_1D_array_2 = np.zeros(50, dtype=np.int)
    test_1D_array_2[20:49] = 10
    test_1D_array_3 = np.ones(10, dtype='float')

    test_constant_int = 5
    test_constant_flt = 2.0

    # Int array and int constant
    add_check = test_array_1 + test_constant_int
    sub_check = np.subtract(test_array_1, test_constant_int)
    mult_check = np.multiply(test_array_1, test_constant_int)
    div_check = np.divide(test_array_1, test_constant_int)

    assert_equal(img.arithmetic('add', test_array_1, test_constant_int),
                 add_check)
    assert_equal(img.arithmetic('subtract', test_array_1,
                                test_constant_int), sub_check)
    assert_equal(img.arithmetic('multiply', test_array_1,
                                test_constant_int), mult_check)
    assert_equal(img.arithmetic('divide', test_array_1, test_constant_int),
                 div_check)
    assert_raises(FloatingPointError, img.arithmetic,  'divide', test_array_1,
                  test_array_1)
    assert_raises(FloatingPointError, img.arithmetic, 'divide', test_array_1, 0)

    # Int array and int array
    add_check = test_array_1 + test_array_2
    sub_check = np.subtract(test_array_1, test_array_2)
    mult_check = np.multiply(test_array_1, test_array_2)

    assert_equal(img.arithmetic('add', test_array_1, test_array_2),
                 add_check)
    assert_equal(img.arithmetic('subtract', test_array_1, test_array_2),
                 sub_check)
    assert_equal(img.arithmetic('multiply', test_array_1, test_array_2,),
                 mult_check)
    assert_raises(FloatingPointError, img.arithmetic, 'divide', test_array_2,
                  test_array_1)

    # Float array and float constant
    add_check = test_array_3 + test_constant_flt
    sub_check = np.subtract(test_array_3, test_constant_flt)
    mult_check = np.multiply(test_array_3, test_constant_flt)
    div_check = np.divide(test_array_3, test_constant_flt)

    assert_equal(img.arithmetic('add', test_array_3, test_constant_flt),
                 add_check)
    assert_equal(img.arithmetic('subtract', test_array_3,
                                test_constant_flt), sub_check)
    assert_equal(img.arithmetic('multiply', test_array_3,
                                test_constant_flt), mult_check)
    assert_equal(img.arithmetic('divide', test_array_3, test_constant_flt),
                 div_check)

    # Float array and float array
    add_check = test_array_3 + test_array_3
    sub_check = np.subtract(test_array_3, test_array_3)
    mult_check = np.multiply(test_array_3, test_array_3)
    div_check = np.divide(test_array_3, test_array_3)

    assert_equal(img.arithmetic('add', test_array_3, test_array_3),
                 add_check)
    assert_equal(img.arithmetic('subtract', test_array_3, test_array_3,),
                 sub_check)
    assert_equal(img.arithmetic('multiply', test_array_3, test_array_3),
                 mult_check)
    assert_equal(img.arithmetic('divide', test_array_3, test_array_3),
                 div_check)
    # Mixed dtypes: Int array and float array
    assert_equal(img.arithmetic('add', test_array_1,
                                test_array_1.astype('float')).dtype, float)
    # Float array and int constant
    assert_equal(img.arithmetic('add', test_array_3,
                                test_constant_int).dtype, float)
    # Int array and float constant
    assert_equal(img.arithmetic('add', test_array_1,
                                test_constant_flt).dtype, float)
    # Mismatched array sizes
    assert_raises(ValueError, img.arithmetic, 'add', test_array_1,
                  test_array_3)


def test_arithmetic_custom():
    """
    Test function for vttools.to_wrap.image_proc.arithmetic_expression,
    a function that allows the inclusion of up to 8 inputs (arrays or
    constants) and application of a custom expression, to simplify image
    arithmetic including 2 or more objects or parameters.
    """
    # TEST DATA
    test_array_1 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_1[10:19, 10:19, 10:19] = 1
    test_array_2 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_2[20:29, 20:29, 20:29] = 2
    test_array_3 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_3[30:39, 30:39, 30:39] = 3
    test_array_4 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_4[40:49, 40:49, 40:49] = 4
    test_array_5 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_5[50:59, 50:59, 50:59] = 5
    test_array_6 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_6[60:69, 60:69, 60:69] = 6
    test_array_7 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_7[70:79, 70:79, 70:79] = 7
    test_array_8 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_8[80:89, 80:89, 80:89] = 8

    # Array manipulation
    # -int only
    result = (test_array_1 + test_array_2 + test_array_3 + test_array_4 +
              test_array_5 + test_array_6 + test_array_7 + test_array_8)

    assert_equal(img.arithmetic_expression('A+B+C+D+E+F+G+H', test_array_1,
                                           test_array_2, test_array_3,
                                           test_array_4, test_array_5,
                                           test_array_6, test_array_7,
                                           test_array_8), result)

    # -float only
    result = ((test_array_1.astype('float') + 3.5) +
              (test_array_3.astype('float') / 2.0) -
              test_array_4.astype('float'))

    assert_equal(img.arithmetic_expression('(A+B)+(C/D)-E',
                                           test_array_1.astype('float'), 3.5,
                                           test_array_3.astype('float'), 2.0,
                                           test_array_4.astype('float')),
                 result)

    # -mixed int and float
    result = ((test_array_1 + 3.5) + (test_array_3.astype('float') / 2) -
              test_array_4)

    assert_equal(img.arithmetic_expression('(A+B)+(C/D)-E', test_array_1, 3.5,
                                           test_array_3.astype('float'), 2,
                                           test_array_4.astype('float')),
                 result)

    assert_equal(img.arithmetic_expression('(A+B)+(C/D)-E', test_array_1, 3.5,
                                           test_array_3.astype('float'), 2,
                                           test_array_4.astype('float')).dtype,
                 float)


def test_logical():
    """
    Test function for mathops.logic_basic, a function that allows for
    logical operations to be performed on one or two arrays or constants
    depending on the type of operation.
    For example:
    logical not only takes one object, and returns the inverse, while the
    other operations provide a comparison of two objects).
    """
    # TEST DATA
    test_array_1 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_1[0:39, 0:39, 0:39] = 1
    test_array_2 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_2[20:79, 20:79, 20:79] = 2
    test_array_3 = np.zeros((90, 90, 90), dtype=np.int)
    test_array_3[40:89, 40:89, 40:89] = 3

    # and
    assert_equal(img.logical('and', test_array_1, test_array_1), test_array_1)

    test_result = img.logical('and', test_array_1, test_array_2)
    assert_equal(test_result[20:39, 20:39, 20:39], True)
    assert_equal(test_result.sum(), ((39-20)**3))

    assert_equal(img.logical('and', test_array_1, test_array_3), False)

    # or
    assert_equal(img.logical('or', test_array_1, test_array_1), test_array_1)

    assert_equal(img.logical('or', test_array_1, test_array_2).sum(),
                 (test_array_1.sum() + test_array_2.sum() / 2 -
                  np.logical_and(test_array_1, test_array_2).sum()))

    test_result = img.logical('or', test_array_1, test_array_3)
    assert_equal(test_result.sum(), (test_array_1.sum() + test_array_3.sum() /
                                     test_array_3.max()))

    # not
    assert_equal(img.logical('not', test_array_1).sum(),
                 (90**3-test_array_1.sum()))

    assert_equal(img.logical('not', test_array_3).sum(),
                 (90**3-(test_array_3.sum()/test_array_3.max())))

    # xor
    assert_equal(img.logical('xor', test_array_1, test_array_1),
                 np.zeros((90, 90, 90), dtype=np.int))

    assert_equal(img.logical('xor', test_array_1, test_array_2).sum(),
                 ((test_array_1.sum() + test_array_2.sum() / 2) -
                  (2 * np.logical_and(test_array_1, test_array_2).sum())))

    # nand
    assert_equal(img.logical('nand', test_array_1, test_array_1),
                 np.logical_not(test_array_1))

    test_result = img.logical('nand', test_array_1, test_array_2)
    assert_equal(test_result[20:39, 20:39, 20:39], False)

    # nor
    assert_equal(img.logical('nor', test_array_1, test_array_1),
                 np.logical_not(test_array_1))
    assert_equal(img.logical('nor', test_array_1, test_array_2).sum(),
                 (np.ones((90, 90, 90), dtype=np.int).sum() -
                  (np.logical_or(test_array_1, test_array_2).sum())))

    # subtract
    assert_equal(img.logical('sub', test_array_1, test_array_1), False)

    test_result = img.logical('sub', test_array_1, test_array_2)
    assert_equal(test_result[20:39, 20:39, 20:39], False)

    assert_equal(test_result.sum(), (test_array_1.sum() -
                                     np.logical_and(test_array_1,
                                                    test_array_2).sum()))

    test_result = img.logical('sub', test_array_1, test_array_3)
    assert_equal(test_result, test_array_1)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)
