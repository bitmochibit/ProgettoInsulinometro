def from_hex(num) -> str:
    """
    Converts a hex UUID in the form 0x<any_number> (string or integer) to a UUID string.

    Args:
        num (str or int): The input hexadecimal number, e.g., '0xAB2C' or 0xAB2C.

    Returns:
        str: A formatted UUID string in the form '0000<any_number>-0000-1000-8000-00805f9b34fb',
             with the hex portion lowercased.

    Raises:
        ValueError: If the input is not a valid hexadecimal string or integer.
    """
    # Handle string input
    if isinstance(num, str):
        if not num.startswith("0x") or not all(c in "0123456789abcdefABCDEF" for c in num[2:]):
            raise ValueError("Input must be a hexadecimal string starting with '0x'.")
        hex_part = num[2:].lower()
    # Handle integer input
    elif isinstance(num, int):
        if num < 0:
            raise ValueError("Hexadecimal input must be a positive integer.")
        hex_part = f"{num:x}"  # Convert integer to lowercase hex
    else:
        raise ValueError("Input must be a hexadecimal string or an integer.")

    # Format and return the UUID
    return f"0000{hex_part}-0000-1000-8000-00805f9b34fb"
