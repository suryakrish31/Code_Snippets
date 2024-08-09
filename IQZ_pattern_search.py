def hex_string_to_bytes(hex_string):
    return bytearray.fromhex(''.join(hex_string.split()))

def int_to_3bit_binary(num):
    # Convert integer to binary string
    binary_str = bin(num)[2:]
    # Ensure the string is exactly 3 bits long
    binary_str = binary_str.zfill(3)
    return binary_str

def modify_byte_array(i_array, q_array, z_array, iqz):
    output_i_array = []
    output_q_array = []
    output_z_array = []
    iqz = int_to_3bit_binary(iqz)
    if iqz[0] == '0':
        output_i_array = [x ^ 1 for x in i_array]
    else:
        output_i_array = i_array
    if iqz[1] == '0':
        output_q_array = [x ^ 1 for x in q_array]
    else:
        output_q_array = q_array
    if iqz[2] == '0':
        output_z_array = [x ^ 1 for x in z_array]
    else:
        output_z_array = z_array

    print("Modified I Array: IQZ: ",iqz, output_i_array)
    print("Modified Q Array: IQZ: ",iqz, output_q_array)
    print("Modified Z Array: IQZ: ",iqz, output_z_array, "\n")
    return output_i_array, output_q_array, output_z_array

def create_iqz_arrays(byte_array):
    i_array = []
    q_array = []
    z_array = []

    for i in range(len(byte_array) * 8):  # Total number of bits in the byte array
        byte_index = i // 8
        bit_index = i % 8

        byte = byte_array[byte_index]

        if i % 3 == 0:
            i_bit = (byte >> bit_index) & 0b00000001
            i_array.append(i_bit)
        elif i % 3 == 1:
            q_bit = (byte >> bit_index) & 0b00000001
            q_array.append(q_bit)
        else:
            z_bit = (byte >> bit_index) & 0b00000001
            z_array.append(z_bit)

    return i_array, q_array, z_array

def reconstruct_byte_array(i_array, q_array, z_array):
    byte_array = bytearray()

    # Ensure all arrays have the same length
    num_bytes = (len(i_array) + len(q_array) + len(z_array))/8

    # Iterate over the bit arrays and interleave the bits
    switch = 0
    k = 0
    for i in range(int(num_bytes)):
        byte = 0
        for j in range(8):
            # Shift each bit to its corresponding position in the byte
            if switch == 0:
                new_bit = i_array[k]
                byte = byte << 1
                byte |= new_bit
                switch = 1
            elif switch == 1:
                new_bit = q_array[k]
                byte = byte << 1
                byte |= new_bit
                switch = 2
            elif switch == 2:
                new_bit = z_array[k]
                byte = byte << 1
                byte |= new_bit
                switch = 0
                k += 1
        byte_array.append(byte)

    return byte_array

def circular_right_bit_shift(byte_array, shift):
    shifted_array = bytearray(len(byte_array))
    msb_bit = 0
    for i in range(len(byte_array)):
        shifted_byte = 0
        lsb_bit = byte_array[i] & 0x01
        shifted_byte |= byte_array[i] >> shift
        shifted_byte |= msb_bit
        msb_bit = lsb_bit << 7
        shifted_array[i] = shifted_byte
    shifted_array[0] |= msb_bit
    return shifted_array

def main2():
    byte_array_input = input("Enter the byte array (e.g., 0x01 0x02 0x03): ")
    byte_array = bytearray.fromhex(''.join(byte_array_input.split()))
    i_array, q_array, z_array = create_iqz_arrays(byte_array)
    print("I Array:", i_array)
    print("Q Array:", q_array)
    print("Z Array:", z_array)

    # shifted_array = circular_right_bit_shift(byte_array, 1)
    # print("Shifted array: ", shifted_array.hex())

    output_arrays = []
    for iqz in range(8):
        output_i_array, output_q_array, output_z_array = modify_byte_array(i_array, q_array, z_array, iqz)
        byte_array_r = reconstruct_byte_array(output_i_array, output_q_array, output_z_array)
        output_arrays.append(byte_array_r)
        # print("Modified Byte Array: IQZ:",iqz, byte_array.hex())

    print("Modified arrays:")
    for i, arr in enumerate(output_arrays):
        print(f"Array {int_to_3bit_binary(i)} : {arr.hex()}")
        shifted_array = output_arrays[i]
        for j in range(len(shifted_array)*8):
            shifted_array = circular_right_bit_shift(shifted_array, 1)
            print("Shifted array: ", shifted_array.hex())


def find_byte_pattern_in_file(byte_pattern, file_path):
    pattern_length = len(byte_pattern)
    if pattern_length == 0:
        return []

    matches = []
    with open(file_path, 'rb') as file:
        current_byte = file.read(1)
        byte_index = 0
        bit_index = 0
        match_start = 0

        while current_byte:
            # Extract the current bit
            current_bit = (current_byte[0] >> (7 - bit_index)) & 0x01

            # Check if the current bit matches the corresponding bit in the pattern
            if current_bit == (byte_pattern[byte_index] >> (7 - bit_index)) & 0x01:
                if bit_index == 0:
                    match_start = file.tell() - 1  # Start of the match

                bit_index += 1
                if bit_index == 8:
                    byte_index += 1
                    bit_index = 0

                if byte_index == pattern_length:
                    matches.append(match_start)
                    byte_index = 0
                    bit_index = 0
            else:
                # If a partial match occurred, reset indices to continue from the next bit
                if bit_index > 0:
                    file.seek(match_start + 1)
                    byte_index = 0
                    bit_index = 0
                else:
                    # If no match occurred, move to the next bit
                    file.seek(file.tell() - 1)

            # Read the next byte from the file
            next_byte = file.read(1)
            if not next_byte:
                break

            # Update current_byte
            current_byte = bytes([(current_byte[0] << 1 | (next_byte[0] >> 7)) & 0xFF])

    return matches
def main():
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    in_file = file_path + input("Enter the input IQ file including path:-\n").strip()

    # Test the function
    byte_pattern = bytearray(b'\xb7')  # Example byte pattern

    matches = find_byte_pattern_in_file(byte_pattern, in_file)
    print("Matches found at positions:", matches)

if __name__ == "__main__":
    main2()