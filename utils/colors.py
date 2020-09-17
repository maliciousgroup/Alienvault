def colors() -> dict:
    """
    Function that returns a dict of different ansi colors

    :return: dict
    """
    _colors: dict = {
        'red': '\x1b[31;1m',
        'blue': '\x1b[36;1m',
        'pink': '\x1b[35;1m',
        'green': '\x1b[32;1m',
        'yellow': '\x1b[33;1m',
        'bold': '\x1b[1m',
        'reset': '\x1b[0m'
    }
    return _colors
