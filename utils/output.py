def write_to_file(filename: str, content: str, mode: str = 'a'):
    """
    Function to write content to a file if permissions allow

    :param filename: The filename to write results to
    :type filename: str
    :param content: Contents to be written to filename
    :type content: str
    :param mode: Mode when writing to file, defaults to 'a'
    :type mode: str (single char)
    :return: None
    """
    try:
        with open(filename, mode, encoding="utf-8") as fd:
            fd.write(content)
    except (NameError, OSError):
        pass
    return
