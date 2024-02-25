def complex_operation(number):
    """
    Perform a series of mathematical operations on the input number.

    Parameters:
    - number (float or int): The input number on which the operations are performed.

    Returns:
    float or int: The result of the complex mathematical operations.
    """
    step1 = number * 5
    step2 = step1 / 6
    step3 = step2 + number - 6
    result = step3 * 6

    return result