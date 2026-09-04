# https://www.geeksforgeeks.org/python-docstrings/

# An ideal Python docstring should be clear, concise, and follow the conventions outlined in PEP 257. It should describe the purpose of the function, class, or module, its parameters, return values, and any exceptions raised. Here's an example of an ideal docstring for a function:

# Copy the code
# def calculate_area(length, width):
#     """
#     Calculate the area of a rectangle.

#     This function takes the length and width of a rectangle as input
#     and returns the calculated area.

#     Args:
#         length (float): The length of the rectangle. Must be a positive number.
#         width (float): The width of the rectangle. Must be a positive number.

#     Returns:
#         float: The area of the rectangle.

#     Raises:
#         ValueError: If either `length` or `width` is not a positive number.

#     Example:
#         >>> calculate_area(5, 3)
#         15.0
#     """
#     if length <= 0 or width <= 0:
#         raise ValueError("Length and width must be positive numbers.")
#     return length * width

# Key Features of an Ideal Docstring:
# Summary Line: A brief description of the function's purpose.
# Detailed Description: (Optional) Additional details about the functionality.
# Args Section: Lists and describes all parameters.
# Returns Section: Explains what the function returns.
# Raises Section: Describes any exceptions the function might raise.
# Example Usage: (Optional) Demonstrates how to use the function.

# This format ensures clarity and makes your code easier to understand and maintain.