"""Preprocessing function for text data."""

from unidecode import unidecode
import re


def to_ascii(text: str) -> str:
    """Converts unicode data to ASCII.

    Parameters
    ----------
    text : str
        text data in string form.

    Returns
    -------
    str
        converted text data.
    """

    return unidecode(text)


def to_alpha(text: str) -> str:
    """Converts text data to alpha, that is, lowercase a-z letters.

    Parameters
    ----------
    text : str
        text data in string form

    Returns
    -------
    str
        converted text data.
    """

    return re.sub(r'[^a-z]', '', to_ascii(text).lower())
