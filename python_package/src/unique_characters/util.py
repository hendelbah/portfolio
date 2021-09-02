import collections
from functools import lru_cache


@lru_cache
def find_unique_characters(string: str) -> list:
    """
    Return list or unique characters of given string (that occurs only once)
    :param string: sequence of characters
    :return: list
    """
    if not isinstance(string, str):
        raise TypeError("argument must be a string")
    char_counter = collections.Counter(string)
    return [char for char, count in char_counter.items() if count == 1]
