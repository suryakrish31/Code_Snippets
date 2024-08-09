def search_pattern_bit_by_bit(data, pattern):
    """
    Search for a specified byte pattern bit by bit within a larger byte sequence.

    Args:
        data (bytes): The byte sequence to search in.
        pattern (bytes): The byte pattern to search for.

    Returns:
        list: List of starting indices where the pattern was found bit by bit.
    """

    def bit_pattern_match(data, pattern, bit_offset):
        """
        Check if pattern matches data starting from a specific bit offset.

        Args:
            data (bytes): The byte sequence to check.
            pattern (bytes): The byte pattern to check against.
            bit_offset (int): The bit offset to start checking from.

        Returns:
            bool: True if the pattern matches, False otherwise.
        """
        byte_offset = bit_offset // 8
        bit_remainder = bit_offset % 8

        for i in range(len(pattern)):
            data_byte_index = byte_offset + i
            if data_byte_index >= len(data):
                return False

            data_byte = data[data_byte_index]
            pattern_byte = pattern[i]

            if bit_remainder == 0:
                if data_byte != pattern_byte:
                    return False
            else:
                # Get bits from current and next byte
                combined_bits = (data_byte << 8) | (data[data_byte_index + 1] if data_byte_index + 1 < len(data) else 0)
                combined_bits >>= (8 - bit_remainder)
                if (combined_bits & 0xFF) != pattern_byte:
                    return False

        return True

    pattern_len_bits = len(pattern) * 8
    data_len_bits = len(data) * 8

    matches = []

    for bit_offset in range(data_len_bits - pattern_len_bits + 1):
        if bit_pattern_match(data, pattern, bit_offset):
            matches.append(bit_offset/8)

    return matches


def read_binary_file(file_path):
    """
    Read the contents of a binary file.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        bytes: The contents of the file.
    """
    with open(file_path, 'rb') as file:
        return file.read()


if __name__ == '__main__':
    # Example usage:
    file_path = r"C:\Users\Admin\Documents\gnu_sinks\\"
    # file = file_path + "consetallation_decoder_output_bpsk_map_check1.bin"
    file = file_path + "fec_decoded_output_bpsk.bin"
    # file_path = 'input.bin'  # Specify the path to your binary file
    pattern = b'\x1a\xcf\xfc\x1d'  # Specify the byte pattern to search for

    data = read_binary_file(file)
    matches = search_pattern_bit_by_bit(data, pattern)
    print("Pattern found at bit offsets:", matches)
