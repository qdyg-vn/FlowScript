def reader(file: str):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                yield line
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' not found.")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Failed to decode '{file}' with utf-8. Error {e}")
    except Exception as e:
        raise Exception(f"Unexpected error when reading file '{file}'. Error {e}")
