def factorial(n):
    """
    Calculate the factorial of a given number.

    Args:
        n (int): The input integer for which the factorial is to be calculated.

    Returns:
        int: The factorial of the input integer.

    Raises:
        ValueError: If the input is a negative integer.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    
    result = 1
    while n > 1:
        result *= n
        n -= 1
    return result

def main():
    number = 5
    result = factorial(number)
    print(f"The factorial of {number} is: {result}")

if __name__ == "__main__":
    main()
