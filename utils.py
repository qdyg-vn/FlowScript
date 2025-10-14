def reader(file):
    """
    Read and return the contents of a UTF-8 encoded text file.

    Parameters:
        file (str): Path to the file to read.

    Returns:
        str: Entire contents of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file cannot be decoded with UTF-8.
        Exception: For any other unexpected errors during file reading.
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()
        return code
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' not found.")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Failed to decode '{file}' with utf-8. Error {e}")
    except Exception as e:
        raise Exception(f"Unexpected error when reading file '{file}'. Error {e}")
