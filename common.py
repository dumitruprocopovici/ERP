""" Common module
implement commonly used functions here
"""

import random


def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation:
         - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letter
         - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """
    generated = ''
    special_characters_list = ["!", "@", "#", "$", "%", "^", "&", "*"]
    lower_case_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                       "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "x", "y", "w", "z"]
    upper_case_list = [i.upper() for i in lower_case_list]

    def random_list(list):
        return random.choice(list)

    for i in range(0, 2):
        generated += random_list(lower_case_list)
        generated += random_list(upper_case_list)
        generated += str(random.randint(0, 9))
        generated += random_list(special_characters_list)

    for i in table:
        if i[0] == generated:
            generated = generate_random(table)

    return generated
